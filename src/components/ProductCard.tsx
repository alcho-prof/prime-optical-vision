import React from 'react';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ShoppingCart, Eye, Heart } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

interface ProductCardProps {
  product: {
    id: string;
    name: string;
    description: string;
    price: number;
    original_price?: number;
    discount_percentage: number;
    image_url: string;
    category: string;
    brand: string;
    featured: boolean;
    uv_protection: boolean;
    anti_glare: boolean;
    scratch_resistant: boolean;
    stock_quantity: number;
  };
  onAddToCart?: (productId: string) => void;
  onViewDetails?: (productId: string) => void;
}

const ProductCard: React.FC<ProductCardProps> = ({ product, onAddToCart, onViewDetails }) => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const discountedPrice = product.original_price && product.discount_percentage > 0 
    ? product.original_price * (1 - product.discount_percentage / 100)
    : product.price;

  const handleAddToCart = () => {
    if (!user) {
      navigate('/auth');
      return;
    }
    onAddToCart?.(product.id);
  };

  const handleViewDetails = () => {
    onViewDetails?.(product.id);
  };

  return (
    <Card className="group hover:shadow-lg transition-all duration-300 overflow-hidden">
      <div className="relative overflow-hidden">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="w-full h-48 bg-muted flex items-center justify-center">
            <Eye className="w-12 h-12 text-muted-foreground" />
          </div>
        )}
        
        {/* Badges */}
        <div className="absolute top-2 left-2 flex flex-wrap gap-1">
          {product.featured && (
            <Badge variant="default" className="text-xs">
              Featured
            </Badge>
          )}
          {product.discount_percentage > 0 && (
            <Badge variant="destructive" className="text-xs">
              {product.discount_percentage}% OFF
            </Badge>
          )}
        </div>

        {/* Wishlist button */}
        <Button
          variant="ghost"
          size="icon"
          className="absolute top-2 right-2 bg-white/80 hover:bg-white"
        >
          <Heart className="w-4 h-4" />
        </Button>

        {/* Stock status */}
        {product.stock_quantity === 0 && (
          <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
            <Badge variant="destructive" className="text-sm">
              Out of Stock
            </Badge>
          </div>
        )}
      </div>

      <CardContent className="p-4">
        <div className="space-y-2">
          {/* Brand */}
          {product.brand && (
            <p className="text-xs text-muted-foreground uppercase tracking-wide">
              {product.brand}
            </p>
          )}

          {/* Product name */}
          <h3 className="font-semibold text-lg line-clamp-2 group-hover:text-primary transition-colors">
            {product.name}
          </h3>

          {/* Category */}
          <Badge variant="outline" className="text-xs">
            {product.category}
          </Badge>

          {/* Features */}
          <div className="flex flex-wrap gap-1">
            {product.uv_protection && (
              <Badge variant="secondary" className="text-xs">
                UV Protection
              </Badge>
            )}
            {product.anti_glare && (
              <Badge variant="secondary" className="text-xs">
                Anti-Glare
              </Badge>
            )}
            {product.scratch_resistant && (
              <Badge variant="secondary" className="text-xs">
                Scratch Resistant
              </Badge>
            )}
          </div>

          {/* Description */}
          {product.description && (
            <p className="text-sm text-muted-foreground line-clamp-2">
              {product.description}
            </p>
          )}

          {/* Price */}
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-primary">
              ₹{discountedPrice.toLocaleString()}
            </span>
            {product.original_price && product.original_price > discountedPrice && (
              <span className="text-sm text-muted-foreground line-through">
                ₹{product.original_price.toLocaleString()}
              </span>
            )}
          </div>
        </div>
      </CardContent>

      <CardFooter className="p-4 pt-0">
        <div className="flex gap-2 w-full">
          <Button
            variant="outline"
            className="flex-1"
            onClick={handleViewDetails}
          >
            <Eye className="w-4 h-4 mr-2" />
            View
          </Button>
          <Button
            className="flex-1"
            onClick={handleAddToCart}
            disabled={product.stock_quantity === 0}
          >
            <ShoppingCart className="w-4 h-4 mr-2" />
            {product.stock_quantity === 0 ? 'Out of Stock' : 'Add to Cart'}
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
};

export default ProductCard;