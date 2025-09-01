import { Card, CardContent } from "@/components/ui/card";
import { Eye, Shield, Award, Users } from "lucide-react";

const features = [
  {
    icon: Eye,
    title: "विशेषज्ञ नेत्र देखभाल",
    description: "वर्षों के अनुभव के साथ प्रमाणित optometrists द्वारा comprehensive eye examinations।"
  },
  {
    icon: Shield,
    title: "गुणवत्ता की गारंटी",
    description: "हमारी जीवनभर quality guarantee के साथ premium materials और craftsmanship।"
  },
  {
    icon: Award,
    title: "पुरस्कार विजेता",
    description: "Optical care और customer satisfaction में excellence के लिए पहचाने गए।"
  },
  {
    icon: Users,
    title: "हजारों का भरोसा",
    description: "10,000+ संतुष्ट ग्राहक अपनी vision needs के लिए हम पर भरोसा करते हैं।"
  }
];

const AboutSection = () => {
  return (
    <section id="about" className="py-20">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            प्राइम ऑप्टिकल्स क्यों चुनें?
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            हम exceptional vision care और premium eyewear solutions देने के लिए दशकों की optical expertise को cutting-edge technology के साथ मिलाते हैं।
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
              <div className="text-muted-foreground text-lg">वर्षों का अनुभव</div>
            </div>
            <div>
              <div className="text-4xl md:text-5xl font-bold text-primary mb-2">10K+</div>
              <div className="text-muted-foreground text-lg">खुश ग्राहक</div>
            </div>
            <div>
              <div className="text-4xl md:text-5xl font-bold text-primary mb-2">500+</div>
              <div className="text-muted-foreground text-lg">फ्रेम स्टाइल्स</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;