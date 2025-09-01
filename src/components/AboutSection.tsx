import { Card, CardContent } from "@/components/ui/card";
import { Eye, Shield, Award, Users } from "lucide-react";

const features = [
  {
    icon: Eye,
    title: "Expert Eye Care",
    description: "Comprehensive eye examinations by certified optometrists with years of experience."
  },
  {
    icon: Shield,
    title: "Quality Guarantee",
    description: "Premium materials and craftsmanship backed by our lifetime quality guarantee."
  },
  {
    icon: Award,
    title: "Award Winning",
    description: "Recognized for excellence in optical care and customer satisfaction."
  },
  {
    icon: Users,
    title: "Trusted by Thousands",
    description: "Over 10,000+ satisfied customers trust us with their vision needs."
  }
];

const AboutSection = () => {
  return (
    <section id="about" className="py-20">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            Why Choose Prime Opticals?
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            We combine decades of optical expertise with cutting-edge technology to deliver 
            exceptional vision care and premium eyewear solutions.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="text-center hover:shadow-violet transition-all duration-300 hover:-translate-y-1 gradient-card border-0"
            >
              <CardContent className="p-8">
                <div className="mb-6 flex justify-center">
                  <div className="p-4 gradient-primary rounded-full shadow-violet animate-glow">
                    <feature.icon className="h-8 w-8 text-white" />
                  </div>
                </div>
                <h3 className="text-xl font-bold mb-3 text-foreground">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Stats Section */}
        <div className="bg-gradient-to-r from-primary/10 to-accent/10 rounded-2xl p-8 md:p-12">
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl md:text-5xl font-bold text-primary mb-2">15+</div>
              <div className="text-muted-foreground text-lg">Years of Experience</div>
            </div>
            <div>
              <div className="text-4xl md:text-5xl font-bold text-primary mb-2">10K+</div>
              <div className="text-muted-foreground text-lg">Happy Customers</div>
            </div>
            <div>
              <div className="text-4xl md:text-5xl font-bold text-primary mb-2">500+</div>
              <div className="text-muted-foreground text-lg">Frame Styles</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;