#include <unordered_map> 
#include <iostream>
#include <optional>
#include <string> 

struct Order {
    int id;
    double price;
    double quantity; 
    std::string side;
    
    friend std::ostream& operator<<(std::ostream& os, const Order& order) {
        os << "[ID: " << order.id 
           << ", Price: $" << order.price 
           << ", Status: " << order.side << "]";
        return os;
    }
};

class SimpleOrderBook{
    private:
        std::unordered_map<int, Order> orders{};        

    public:
        SimpleOrderBook() = default;

    std::optional<Order> getOrder(int order_id){
        auto it = orders.find(order_id);
        if (it != orders.end()){
            return it->second;
        }
        return std::nullopt;
    }
    
    
    bool cancelOrder(int order_id){
        auto order = orders.extract(order_id);
        return !order.empty();
    }

    bool addOrder(Order order){
        if(orders.contains(order.id)){
            return false;
        }
        orders.insert({order.id, order});
        return true;
    }

    void printOrders(){
        for (const auto& [id, order] : orders) { 
            std::cout << "Order: " << order << "\n";
        }
    }

};


int main(){
    SimpleOrderBook book{};
    Order o{.id=1, .price=100.0, .quantity=1, .side= "BUY"};
    book.addOrder(o);
    Order o = book.getOrder(o.id);
    book.printOrders();
    book.cancelOrder(o.id);

}