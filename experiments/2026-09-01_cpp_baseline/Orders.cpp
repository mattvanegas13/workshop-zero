enum class OrderSide {
    BUY, 
    SELL
};

struct Order {
    int id;
    float price;
    OrderSide side;
};


