import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import collectionImage from "@/assets/glasses-collection.jpg";

const collections = [
  {
    id: 1,
    name: "Classic Frames",
    description: "Timeless designs that never go out of style",
    price: "From ₹7,999",
    image: collectionImage,
  },
  {
    id: 2,
    name: "Sports Collection",
    description: "Performance eyewear for active lifestyles",
    price: "From ₹11,999",
    image: collectionImage,
  },
  {
    id: 3,
    name: "Designer Series",
    description: "Luxury frames from premium brands",
    price: "From ₹24,999",
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
            Featured Collections
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Explore our carefully curated selection of premium eyewear designed to enhance your vision and style.
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
            View All Collections
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </div>
    </section>
  );
};

export default FeaturedCollections;