import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { MapPin, Phone, Mail, Clock } from "lucide-react";

const contactInfo = [
  {
    icon: MapPin,
    title: "Visit Our Store",
    details: "123 Main Road, Connaught Place\nNew Delhi 110001"
  },
  {
    icon: Phone,
    title: "Call Us",
    details: "+91 98765 43210\nToll-free: 1800-OPTICALS"
  },
  {
    icon: Mail,
    title: "Email Us",
    details: "info@primeopticals.in\nsupport@primeopticals.in"
  },
  {
    icon: Clock,
    title: "Store Hours",
    details: "Mon-Fri: 9AM - 7PM\nSat-Sun: 10AM - 6PM"
  }
];

const ContactSection = () => {
  return (
    <section id="contact" className="py-20 bg-muted/30">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            Get In Touch
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Ready to find your perfect eyewear? Visit our store or contact us today for a personalized consultation.
          </p>
        </div>

        {/* Contact Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {contactInfo.map((contact, index) => (
            <Card 
              key={index} 
              className="hover:shadow-violet transition-all duration-300 hover:-translate-y-1 gradient-card border-0"
            >
              <CardContent className="p-6 text-center">
                <div className="mb-4 flex justify-center">
                  <div className="p-3 gradient-primary rounded-full">
                    <contact.icon className="h-6 w-6 text-white" />
                  </div>
                </div>
                <h3 className="font-bold mb-2 text-foreground">
                  {contact.title}
                </h3>
                <p className="text-muted-foreground text-sm whitespace-pre-line">
                  {contact.details}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* CTA Section */}
        <div className="bg-gradient-to-r from-primary to-accent rounded-2xl p-8 md:p-12 text-center text-white">
          <h3 className="text-3xl md:text-4xl font-bold mb-4">
            Book Your Eye Examination
          </h3>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Schedule a comprehensive eye exam with our certified optometrists. 
            Early detection and proper vision care are essential for your eye health.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg" 
              variant="secondary"
              className="bg-white text-primary hover:bg-white/90 text-lg px-8 py-6"
            >
              Book Appointment
            </Button>
            <Button 
              size="lg" 
              variant="outline"
              className="border-white/30 text-white hover:bg-white/10 text-lg px-8 py-6"
            >
              Virtual Consultation
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;