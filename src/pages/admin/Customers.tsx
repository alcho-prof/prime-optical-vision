import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { supabase } from '@/integrations/supabase/client';
import { Search, Users, Mail, Phone, ShoppingBag, Eye } from 'lucide-react';
import { toast } from '@/hooks/use-toast';

interface Customer {
  id: string;
  user_id: string;
  full_name: string;
  email: string;
  phone?: string;
  created_at: string;
  updated_at: string;
  orders: Order[];
}

interface Order {
  id: string;
  total_amount: number;
  status: string;
  created_at: string;
}

const Customers = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) throw error;
      
      // Fetch orders separately for each customer
      const customersWithOrders = await Promise.all(
        (data || []).map(async (customer) => {
          const { data: orders } = await supabase
            .from('orders')
            .select('id, total_amount, status, created_at')
            .eq('user_id', customer.user_id);
          
          return { ...customer, orders: orders || [] };
        })
      );
      
      setCustomers(customersWithOrders);
    } catch (error: any) {
      toast({
        title: 'Error fetching customers',
        description: error.message,
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  const getCustomerStats = (customer: Customer) => {
    const totalOrders = customer.orders?.length || 0;
    const totalSpent = customer.orders?.reduce((sum, order) => sum + order.total_amount, 0) || 0;
    const lastOrder = customer.orders?.[0];
    
    return { totalOrders, totalSpent, lastOrder };
  };

  const filteredCustomers = customers.filter(customer => 
    customer.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.phone?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-500"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Customer Management</h1>
          <p className="text-gray-600">View and manage customer information</p>
        </div>
        <div className="flex items-center space-x-4">
          <Card className="px-4 py-2">
            <div className="flex items-center space-x-2">
              <Users className="w-5 h-5 text-amber-600" />
              <div className="text-center">
                <p className="text-sm text-gray-600">Total Customers</p>
                <p className="text-xl font-bold text-gray-900">{customers.length}</p>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Search */}
      <Card>
        <CardContent className="p-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <Input
              placeholder="Search customers by name, email, or phone..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </CardContent>
      </Card>

      {/* Customers Grid */}
      <div className="grid gap-4">
        {filteredCustomers.map((customer) => {
          const { totalOrders, totalSpent, lastOrder } = getCustomerStats(customer);
          
          return (
            <Card key={customer.id} className="hover:shadow-md transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center">
                      <span className="text-white font-semibold text-lg">
                        {customer.full_name?.charAt(0)?.toUpperCase() || 'U'}
                      </span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">
                        {customer.full_name || 'Unknown Customer'}
                      </h3>
                      <div className="flex items-center space-x-4 text-sm text-gray-600">
                        <div className="flex items-center">
                          <Mail className="w-4 h-4 mr-1" />
                          {customer.email}
                        </div>
                        {customer.phone && (
                          <div className="flex items-center">
                            <Phone className="w-4 h-4 mr-1" />
                            {customer.phone}
                          </div>
                        )}
                      </div>
                      <p className="text-xs text-gray-500">
                        Joined {new Date(customer.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-6">
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Orders</p>
                      <p className="text-xl font-bold text-gray-900">{totalOrders}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Total Spent</p>
                      <p className="text-xl font-bold text-green-600">
                        ₹{totalSpent.toLocaleString()}
                      </p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Last Order</p>
                      <p className="text-sm text-gray-900">
                        {lastOrder 
                          ? new Date(lastOrder.created_at).toLocaleDateString()
                          : 'Never'
                        }
                      </p>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setSelectedCustomer(customer)}
                    >
                      <Eye className="w-4 h-4 mr-1" />
                      View Details
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {filteredCustomers.length === 0 && (
        <Card>
          <CardContent className="p-12 text-center">
            <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No customers found</h3>
            <p className="text-gray-600">
              {searchTerm 
                ? 'Try adjusting your search criteria'
                : 'Customers will appear here when they register'
              }
            </p>
          </CardContent>
        </Card>
      )}

      {/* Customer Details Modal */}
      {selectedCustomer && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[80vh] overflow-y-auto">
            <div className="p-6 border-b">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold">Customer Details</h2>
                <Button
                  variant="ghost"
                  onClick={() => setSelectedCustomer(null)}
                >
                  ×
                </Button>
              </div>
            </div>
            <div className="p-6 space-y-6">
              {/* Customer Info */}
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <h3 className="font-medium mb-3">Personal Information</h3>
                  <div className="space-y-2">
                    <p><span className="font-medium">Name:</span> {selectedCustomer.full_name}</p>
                    <p><span className="font-medium">Email:</span> {selectedCustomer.email}</p>
                    <p><span className="font-medium">Phone:</span> {selectedCustomer.phone || 'Not provided'}</p>
                    <p><span className="font-medium">Joined:</span> {new Date(selectedCustomer.created_at).toLocaleDateString()}</p>
                  </div>
                </div>
                <div>
                  <h3 className="font-medium mb-3">Order Summary</h3>
                  <div className="space-y-2">
                    <p><span className="font-medium">Total Orders:</span> {selectedCustomer.orders?.length || 0}</p>
                    <p><span className="font-medium">Total Spent:</span> ₹{(selectedCustomer.orders?.reduce((sum, order) => sum + order.total_amount, 0) || 0).toLocaleString()}</p>
                    <p><span className="font-medium">Average Order:</span> ₹{selectedCustomer.orders?.length ? Math.round((selectedCustomer.orders.reduce((sum, order) => sum + order.total_amount, 0) / selectedCustomer.orders.length)).toLocaleString() : 0}</p>
                  </div>
                </div>
              </div>

              {/* Order History */}
              <div>
                <h3 className="font-medium mb-3">Order History</h3>
                <div className="space-y-2">
                  {selectedCustomer.orders?.map((order) => (
                    <div key={order.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                      <div>
                        <p className="font-medium">Order #{order.id.slice(0, 8)}</p>
                        <p className="text-sm text-gray-600">{new Date(order.created_at).toLocaleDateString()}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-medium">₹{order.total_amount.toLocaleString()}</p>
                        <Badge className={
                          order.status === 'delivered' ? 'bg-green-100 text-green-800' :
                          order.status === 'shipped' ? 'bg-blue-100 text-blue-800' :
                          order.status === 'confirmed' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }>
                          {order.status}
                        </Badge>
                      </div>
                    </div>
                  )) || (
                    <p className="text-gray-600 text-center py-4">No orders found</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Customers;