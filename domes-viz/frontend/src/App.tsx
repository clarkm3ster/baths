import { ScrollProgress, BackgroundTransition } from "./scroll";
import { OpeningSection } from "./sections/OpeningSection";
import { PromiseSection } from "./sections/PromiseSection";
import { RealitySection } from "./sections/RealitySection";
import { VisionSection } from "./sections/VisionSection";
import { MathSection } from "./sections/MathSection";
import { CallSection } from "./sections/CallSection";
import { Footer } from "./sections/Footer";

function App() {
  return (
    <BackgroundTransition>
      <ScrollProgress />
      <main>
        <OpeningSection />
        <PromiseSection />
        <RealitySection />
        <VisionSection />
        <MathSection />
        <CallSection />
      </main>
      <Footer />
    </BackgroundTransition>
  );
}

export default App;
