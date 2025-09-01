import { Button } from "@/components/ui/button";
import { ArrowRight, Eye } from "lucide-react";
import heroImage from "@/assets/hero-glasses.jpg";

const Hero = () => {
  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 gradient-hero opacity-80"></div>
      <div 
        className="absolute inset-0 bg-cover bg-center opacity-20"
        style={{ backgroundImage: `url(${heroImage})` }}
      ></div>
      
      {/* Content */}
      <div className="relative z-10 container mx-auto px-4 text-center">
        <div className="max-w-4xl mx-auto">
          {/* Icon */}
          <div className="mb-8 flex justify-center">
            <div className="p-4 bg-white/10 backdrop-blur-sm rounded-full shadow-violet animate-float">
              <Eye className="h-12 w-12 text-white" />
            </div>
          </div>
          
          {/* Heading */}
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            India's Premier
            <span className="block bg-gradient-to-r from-white to-violet-200 bg-clip-text text-transparent">
              Eyewear Destination
            </span>
          </h1>
          
          {/* Subheading */}
          <p className="text-xl md:text-2xl text-white/90 mb-10 max-w-2xl mx-auto leading-relaxed">
            Clear Vision, Beautiful Style. Premium eyewear crafted for Indian lifestyles with 
            cutting-edge technology and timeless designs.
          </p>
          
          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button size="lg" className="bg-white text-primary hover:bg-white/90 text-lg px-8 py-6 shadow-violet-lg transition-all duration-300 hover:scale-105">
              Shop Collections
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button 
              variant="outline" 
              size="lg" 
              className="border-white/30 text-white hover:bg-white/10 text-lg px-8 py-6 backdrop-blur-sm"
            >
              Free Eye Test
            </Button>
          </div>
        </div>
      </div>
      
      {/* Bottom gradient fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-background to-transparent"></div>
    </section>
  );
};

export default Hero;