import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import collectionImage from "@/assets/glasses-collection.jpg";

const collections = [
  {
    id: 1,
    name: "क्लासिक फ्रेम्स",
    description: "समयहीन डिज़ाइन जो कभी पुराने नहीं होते",
    price: "₹7,999 से शुरू",
    image: collectionImage,
  },
  {
    id: 2,
    name: "स्पोर्ट्स कलेक्शन",
    description: "सक्रिय जीवनशैली के लिए performance eyewear",
    price: "₹11,999 से शुरू",
    image: collectionImage,
  },
  {
    id: 3,
    name: "डिज़ाइनर सीरीज़",
    description: "प्रीमियम ब्रांड्स के luxury frames",
    price: "₹24,999 से शुरू",
    image: collectionImage,
  },
];

const FeaturedCollections = () => {
  return (
    <section id="collections" className="py-20 bg-muted/30">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            फीचर्ड कलेक्शन्स
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            हमारे सावधानी से चुने गए premium eyewear का संग्रह जो आपकी दृष्टि और style को बढ़ाने के लिए डिज़ाइन किया गया।
          </p>
        </div>

        {/* Collections Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {collections.map((collection, index) => (
            <Card 
              key={collection.id} 
              className="group hover:shadow-violet transition-all duration-500 hover:-translate-y-2 gradient-card border-0 overflow-hidden"
              style={{ animationDelay: `${index * 200}ms` }}
            >
              <CardContent className="p-0">
                {/* Image */}
                <div className="relative overflow-hidden">
                  <img 
                    src={collection.image} 
                    alt={collection.name}
                    className="w-full h-64 object-cover transition-transform duration-500 group-hover:scale-110"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </div>
                
                {/* Content */}
                <div className="p-6">
                  <h3 className="text-2xl font-bold mb-2 text-foreground group-hover:text-primary transition-colors">
                    {collection.name}
                  </h3>
                  <p className="text-muted-foreground mb-4">
                    {collection.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-xl font-semibold text-primary">
                      {collection.price}
                    </span>
                    <Button 
                      variant="ghost" 
                      className="group-hover:bg-primary group-hover:text-primary-foreground transition-all duration-300"
                    >
                      View Collection
                      <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* View All Button */}
        <div className="text-center">
          <Button size="lg" variant="outline" className="border-primary text-primary hover:bg-primary hover:text-primary-foreground shadow-card">
            सभी कलेक्शन्स देखें
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </div>
    </section>
  );
};

export default FeaturedCollections;