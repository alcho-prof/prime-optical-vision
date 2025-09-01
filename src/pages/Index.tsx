import Navigation from "@/components/Navigation";
import Hero from "@/components/Hero";
import FeaturedCollections from "@/components/FeaturedCollections";
import AboutSection from "@/components/AboutSection";
import ContactSection from "@/components/ContactSection";
import Footer from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen">
      <Navigation />
      <Hero />
      <FeaturedCollections />
      <AboutSection />
      <ContactSection />
      <Footer />
    </div>
  );
};

export default Index;
