/**
 * SPHERES Studio — useCostEstimate Hook
 * =======================================
 * Real-time cost estimation hook that debounces API calls and provides
 * reactive cost data as the designer modifies canvas elements.
 *
 * Takes current canvas elements as input, debounces calls to the
 * POST /api/cost/estimate endpoint (300ms), and returns the full
 * cost breakdown including revenue projections and permanence value.
 */

import { useState, useEffect, useRef, useCallback } from "react";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface CanvasElement {
  element_type: string;
  quantity: number;
  custom_unit_cost?: number | null;
  custom_name?: string | null;
}

export interface DesignConfig {
  elements: CanvasElement[];
  duration_days?: number;
  activation_type?: string;
  size_sqft?: number;
  location_score?: number;
  expected_attendance?: number;
  event_type?: string;
  parcel_type?: string;
  permanence_score?: number;
  equity_score?: number;
}

export interface CostBreakdownLine {
  category: string;
  item: string;
  quantity: number;
  unit_cost: number;
  total: number;
}

export interface ElementsCost {
  materials: number;
  labor: number;
  equipment_rental: number;
}

export interface PermitsCost {
  application_fees: number;
  insurance: number;
}

export interface OperationsCost {
  utilities: number;
  staffing: number;
  security: number;
}

export interface RevenueProjections {
  ticket_sales: number;
  vendor_fees: number;
  sponsorship_potential: number;
  grant_eligibility: number;
}

export interface CostEstimate {
  elements_cost: ElementsCost;
  permits_cost: PermitsCost;
  operations_cost: OperationsCost;
  teardown_cost: number;
  permanent_improvements_value: number;
  total_cost: number;
  cost_breakdown: CostBreakdownLine[];
  revenue_projections: RevenueProjections;
  net_projection: number;
  permanence_value: number;
  roi_with_permanence: number;
}

export interface UseCostEstimateReturn {
  costs: CostEstimate | null;
  revenue: RevenueProjections | null;
  net: number;
  permanenceValue: number;
  isLoading: boolean;
  error: string | null;
  breakdown: CostBreakdownLine[];
  totalCost: number;
  roiWithPermanence: number;
  refetch: () => void;
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const DEBOUNCE_MS = 300;
const API_URL = "/api/cost/estimate";

// ---------------------------------------------------------------------------
// Hook
// ---------------------------------------------------------------------------

export function useCostEstimate(config: DesignConfig): UseCostEstimateReturn {
  const [costs, setCosts] = useState<CostEstimate | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  const configRef = useRef(config);
  configRef.current = config;

  // Stable serialization key for change detection
  const configKey = serializeConfig(config);

  const fetchEstimate = useCallback(async () => {
    const currentConfig = configRef.current;

    // Bail if no elements
    if (!currentConfig.elements || currentConfig.elements.length === 0) {
      setCosts(null);
      setError(null);
      setIsLoading(false);
      return;
    }

    // Abort any in-flight request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const controller = new AbortController();
    abortControllerRef.current = controller;

    setIsLoading(true);
    setError(null);

    try {
      const body = {
        elements: currentConfig.elements.map((el) => ({
          element_type: el.element_type,
          quantity: el.quantity,
          ...(el.custom_unit_cost != null && {
            custom_unit_cost: el.custom_unit_cost,
          }),
          ...(el.custom_name != null && { custom_name: el.custom_name }),
        })),
        duration_days: currentConfig.duration_days ?? 1,
        activation_type: currentConfig.activation_type ?? "event",
        size_sqft: currentConfig.size_sqft ?? 1000,
        location_score: currentConfig.location_score ?? 0.5,
        expected_attendance: currentConfig.expected_attendance ?? 100,
        event_type: currentConfig.event_type ?? "community",
        parcel_type: currentConfig.parcel_type ?? "park",
        permanence_score: currentConfig.permanence_score ?? 0.5,
        equity_score: currentConfig.equity_score ?? 0.5,
      };

      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(
          errorData?.detail ??
            `Cost estimation failed: ${response.status} ${response.statusText}`
        );
      }

      const data: CostEstimate = await response.json();
      setCosts(data);
      setError(null);
    } catch (err: unknown) {
      if (err instanceof DOMException && err.name === "AbortError") {
        // Request was cancelled — not an error
        return;
      }
      const message =
        err instanceof Error ? err.message : "Cost estimation failed";
      setError(message);
    } finally {
      if (abortControllerRef.current === controller) {
        setIsLoading(false);
      }
    }
  }, []);

  // Debounced recalculation when config changes
  useEffect(() => {
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }

    debounceTimerRef.current = setTimeout(() => {
      fetchEstimate();
    }, DEBOUNCE_MS);

    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [configKey, fetchEstimate]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, []);

  // Manual refetch
  const refetch = useCallback(() => {
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    fetchEstimate();
  }, [fetchEstimate]);

  return {
    costs,
    revenue: costs?.revenue_projections ?? null,
    net: costs?.net_projection ?? 0,
    permanenceValue: costs?.permanence_value ?? 0,
    isLoading,
    error,
    breakdown: costs?.cost_breakdown ?? [],
    totalCost: costs?.total_cost ?? 0,
    roiWithPermanence: costs?.roi_with_permanence ?? 0,
    refetch,
  };
}

// ---------------------------------------------------------------------------
// Utilities
// ---------------------------------------------------------------------------

/**
 * Produce a stable string key from a DesignConfig for change detection.
 * Uses sorted JSON to ensure consistent ordering.
 */
function serializeConfig(config: DesignConfig): string {
  const normalized = {
    e: config.elements
      .map((el) => `${el.element_type}:${el.quantity}:${el.custom_unit_cost ?? ""}:${el.custom_name ?? ""}`)
      .sort()
      .join("|"),
    d: config.duration_days ?? 1,
    a: config.activation_type ?? "event",
    s: config.size_sqft ?? 1000,
    l: config.location_score ?? 0.5,
    at: config.expected_attendance ?? 100,
    et: config.event_type ?? "community",
    p: config.parcel_type ?? "park",
    ps: config.permanence_score ?? 0.5,
    eq: config.equity_score ?? 0.5,
  };
  return JSON.stringify(normalized);
}

export default useCostEstimate;
