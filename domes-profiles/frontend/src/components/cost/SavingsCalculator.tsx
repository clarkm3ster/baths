/**
 * SavingsCalculator — scale and ROI calculators.
 *
 * Scale: "For N similar people, savings = $X/year"
 * ROI: "Coordination costs $X. Break-even in Y months. 5-year ROI: Z%"
 */

import { useState, useEffect } from 'react';
import { calculateROI, calculateScale } from '../../api/client';
import type { ROIResult, ScaleResult } from '../../types';
import { formatCurrencyFull, formatCurrency } from '../shared/CostDisplay';

interface Props {
  perPersonSavings: number;
  className?: string;
}

const POPULATION_PRESETS = [
  { label: '1,000 people', value: 1000 },
  { label: '10,000 people', value: 10000 },
  { label: '100,000 people', value: 100000 },
  { label: '1,000,000 people', value: 1000000 },
];

export default function SavingsCalculator({ perPersonSavings, className = '' }: Props) {
  const [populationSize, setPopulationSize] = useState(10000);
  const [coordinationCost, setCoordinationCost] = useState(5000000);
  const [roiYears, setRoiYears] = useState(5);
  const [roiResult, setRoiResult] = useState<ROIResult | null>(null);
  const [scaleResult, setScaleResult] = useState<ScaleResult | null>(null);
  const [loadingRoi, setLoadingRoi] = useState(false);
  const [loadingScale, setLoadingScale] = useState(false);

  // Calculate scale on population change
  useEffect(() => {
    setLoadingScale(true);
    calculateScale({
      per_person_savings: perPersonSavings,
      populations: {
        selected: populationSize,
      },
    })
      .then(setScaleResult)
      .catch(() => {
        // Fallback: compute locally
        setScaleResult({
          per_person: perPersonSavings,
          formatted: { selected: formatCurrencyFull(perPersonSavings * populationSize) },
          populations: { selected: perPersonSavings * populationSize },
        });
      })
      .finally(() => setLoadingScale(false));
  }, [perPersonSavings, populationSize]);

  // Calculate ROI on input change
  useEffect(() => {
    if (coordinationCost <= 0 || perPersonSavings <= 0) return;
    setLoadingRoi(true);
    const annualSavings = perPersonSavings * populationSize;
    calculateROI({
      coordination_cost: coordinationCost,
      annual_savings: annualSavings,
      years: roiYears,
    })
      .then(setRoiResult)
      .catch(() => {
        // Fallback: compute locally
        const breakEvenMonths = (coordinationCost / annualSavings) * 12;
        const fiveYearNet = annualSavings * roiYears - coordinationCost;
        const fiveYearRoi = ((fiveYearNet) / coordinationCost) * 100;
        setRoiResult({
          coordination_cost: coordinationCost,
          annual_savings: annualSavings,
          break_even_months: Math.round(breakEvenMonths),
          five_year_roi: Math.round(fiveYearRoi),
          five_year_net: fiveYearNet,
          ten_year_net: annualSavings * 10 - coordinationCost,
        });
      })
      .finally(() => setLoadingRoi(false));
  }, [perPersonSavings, populationSize, coordinationCost, roiYears]);

  const totalSavings = perPersonSavings * populationSize;

  return (
    <div className={`${className}`}>
      {/* ── Scale calculator ── */}
      <div className="mb-10">
        <div className="section-label mb-4">Scale Calculator</div>
        <p className="text-[13px] text-[var(--color-text-secondary)] mb-4">
          What if coordination was applied to an entire population?
        </p>

        {/* Population presets */}
        <div className="flex flex-wrap gap-0 mb-4">
          {POPULATION_PRESETS.map((preset) => (
            <button
              key={preset.value}
              onClick={() => setPopulationSize(preset.value)}
              className={`px-4 py-2 border-2 border-black -ml-[2px] first:ml-0 font-mono text-[12px] uppercase tracking-wider transition-colors ${
                populationSize === preset.value
                  ? 'bg-black text-white'
                  : 'bg-white text-black hover:bg-[var(--color-surface)]'
              }`}
            >
              {preset.label}
            </button>
          ))}
        </div>

        {/* Custom input */}
        <div className="flex items-center gap-3 mb-6">
          <label className="font-mono text-[12px] text-[var(--color-text-tertiary)] uppercase">
            Custom:
          </label>
          <input
            type="number"
            value={populationSize}
            onChange={(e) => setPopulationSize(Math.max(1, parseInt(e.target.value) || 1))}
            className="w-[160px] px-3 py-2 border-2 border-black font-mono text-[14px] bg-white focus:outline-none"
          />
          <span className="text-[13px] text-[var(--color-text-secondary)]">people</span>
        </div>

        {/* Scale result */}
        <div className="border-2 border-black p-6 bg-[var(--color-surface)]">
          <div className="text-[14px] text-[var(--color-text-secondary)] mb-2">
            For{' '}
            <span className="font-mono font-medium text-black">
              {populationSize.toLocaleString()}
            </span>{' '}
            similar people:
          </div>
          <div className="font-mono text-[42px] font-medium text-[var(--color-savings)] leading-none">
            {loadingScale ? '...' : formatCurrency(totalSavings)}
            <span className="text-[16px] text-[var(--color-text-tertiary)]">/year</span>
          </div>
          <div className="text-[12px] text-[var(--color-text-tertiary)] mt-2 font-mono">
            {formatCurrencyFull(perPersonSavings)} per person x {populationSize.toLocaleString()} people
          </div>
        </div>
      </div>

      {/* ── ROI calculator ── */}
      <div>
        <div className="section-label mb-4">ROI Calculator</div>
        <p className="text-[13px] text-[var(--color-text-secondary)] mb-4">
          What does it cost to build the coordination infrastructure,
          and how quickly does it pay for itself?
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          <div>
            <label className="font-mono text-[11px] text-[var(--color-text-tertiary)] uppercase tracking-wider block mb-2">
              Coordination infrastructure cost
            </label>
            <input
              type="number"
              value={coordinationCost}
              onChange={(e) => setCoordinationCost(Math.max(0, parseInt(e.target.value) || 0))}
              className="w-full px-3 py-2 border-2 border-black font-mono text-[14px] bg-white focus:outline-none"
            />
          </div>
          <div>
            <label className="font-mono text-[11px] text-[var(--color-text-tertiary)] uppercase tracking-wider block mb-2">
              Projection period (years)
            </label>
            <input
              type="number"
              value={roiYears}
              min={1}
              max={20}
              onChange={(e) => setRoiYears(Math.max(1, Math.min(20, parseInt(e.target.value) || 5)))}
              className="w-full px-3 py-2 border-2 border-black font-mono text-[14px] bg-white focus:outline-none"
            />
          </div>
        </div>

        {/* ROI results */}
        {roiResult && (
          <div className="border-2 border-black">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-0">
              <div className="p-4 border-r border-b border-[var(--color-border)]">
                <div className="section-label">Break-even</div>
                <div className="font-mono text-[28px] font-medium">
                  {loadingRoi ? '...' : roiResult.break_even_months}
                  <span className="text-[12px] text-[var(--color-text-tertiary)] ml-1">mo</span>
                </div>
              </div>
              <div className="p-4 border-r border-b border-[var(--color-border)]">
                <div className="section-label">{roiYears}-year ROI</div>
                <div className="font-mono text-[28px] font-medium text-[var(--color-savings)]">
                  {loadingRoi ? '...' : `${roiResult.five_year_roi}%`}
                </div>
              </div>
              <div className="p-4 border-r border-b border-[var(--color-border)]">
                <div className="section-label">{roiYears}-year net</div>
                <div className="font-mono text-[28px] font-medium text-[var(--color-savings)]">
                  {loadingRoi ? '...' : formatCurrency(roiResult.five_year_net)}
                </div>
              </div>
              <div className="p-4 border-b border-[var(--color-border)]">
                <div className="section-label">10-year net</div>
                <div className="font-mono text-[28px] font-medium text-[var(--color-savings)]">
                  {loadingRoi ? '...' : formatCurrency(roiResult.ten_year_net)}
                </div>
              </div>
            </div>
            <div className="p-4 bg-[var(--color-surface)] text-[12px] text-[var(--color-text-tertiary)] font-mono">
              Infrastructure: {formatCurrencyFull(coordinationCost)} | Annual savings: {formatCurrency(totalSavings)} | Population: {populationSize.toLocaleString()}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
