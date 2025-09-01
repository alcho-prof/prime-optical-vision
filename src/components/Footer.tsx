import { Facebook, Instagram, Twitter, Youtube } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-foreground text-background py-12">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 gradient-primary rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-sm">P</span>
              </div>
              <span className="text-xl font-bold">Prime Opticals</span>
            </div>
            <p className="text-background/80 mb-4">
              Your trusted partner in vision care, providing premium eyewear and expert optical services.
            </p>
            <div className="flex space-x-4">
              <Facebook className="h-5 w-5 text-background/60 hover:text-background cursor-pointer transition-colors" />
              <Instagram className="h-5 w-5 text-background/60 hover:text-background cursor-pointer transition-colors" />
              <Twitter className="h-5 w-5 text-background/60 hover:text-background cursor-pointer transition-colors" />
              <Youtube className="h-5 w-5 text-background/60 hover:text-background cursor-pointer transition-colors" />
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-bold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-background/80">
              <li><a href="#home" className="hover:text-background transition-colors">Home</a></li>
              <li><a href="#collections" className="hover:text-background transition-colors">Collections</a></li>
              <li><a href="#about" className="hover:text-background transition-colors">About</a></li>
              <li><a href="#contact" className="hover:text-background transition-colors">Contact</a></li>
            </ul>
          </div>

          {/* Services */}
          <div>
            <h3 className="font-bold mb-4">Services</h3>
            <ul className="space-y-2 text-background/80">
              <li><a href="#" className="hover:text-background transition-colors">Eye Examinations</a></li>
              <li><a href="#" className="hover:text-background transition-colors">Contact Lenses</a></li>
              <li><a href="#" className="hover:text-background transition-colors">Frame Fitting</a></li>
              <li><a href="#" className="hover:text-background transition-colors">Repairs</a></li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="font-bold mb-4">Contact Info</h3>
            <div className="space-y-2 text-background/80">
              <p>123 Vision Street</p>
              <p>Downtown, NY 10001</p>
              <p>+1 (555) 123-4567</p>
              <p>info@primeopticals.com</p>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-background/20 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-background/60 text-sm">
            © 2024 Prime Opticals. All rights reserved.
          </p>
          <div className="flex space-x-6 text-sm text-background/60 mt-4 md:mt-0">
            <a href="#" className="hover:text-background transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-background transition-colors">Terms of Service</a>
            <a href="#" className="hover:text-background transition-colors">Cookie Policy</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;