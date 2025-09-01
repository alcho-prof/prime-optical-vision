import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { MapPin, Phone, Mail, Clock } from "lucide-react";

const contactInfo = [
  {
    icon: MapPin,
    title: "हमारे स्टोर पर आएं",
    details: "123 मुख्य मार्ग, कनॉट प्लेस\nनई दिल्ली 110001"
  },
  {
    icon: Phone,
    title: "कॉल करें",
    details: "+91 98765 43210\nToll-free: 1800-OPTICALS"
  },
  {
    icon: Mail,
    title: "ईमेल करें",
    details: "info@primeopticals.in\nsupport@primeopticals.in"
  },
  {
    icon: Clock,
    title: "स्टोर का समय",
    details: "सोम-शुक्र: 9AM - 7PM\nशनि-रवि: 10AM - 6PM"
  }
];

const ContactSection = () => {
  return (
    <section id="contact" className="py-20 bg-muted/30">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            संपर्क में रहें
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            अपना perfect eyewear खोजने के लिए तैयार हैं? व्यक्तिगत consultation के लिए आज ही हमारे store पर आएं या संपर्क करें।
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
            अपनी आंखों की जांच बुक करें
          </h3>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            हमारे प्रमाणित optometrists के साथ comprehensive eye exam schedule करें। 
            Early detection और proper vision care आपकी eye health के लिए आवश्यक है।
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg" 
              variant="secondary"
              className="bg-white text-primary hover:bg-white/90 text-lg px-8 py-6"
            >
              अपॉइंटमेंट बुक करें
            </Button>
            <Button 
              size="lg" 
              variant="outline"
              className="border-white/30 text-white hover:bg-white/10 text-lg px-8 py-6"
            >
              वर्चुअल कंसल्टेशन
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;