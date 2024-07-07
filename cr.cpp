#include <iostream>
#include <cmath>
using namespace std;
struct Point {
    double x;
    double y;
};

struct Circle {
    Point center;
    double radius;
};
bool isPointInsideCircle(const Point& point, const Circle& circle) {
    double distance = std::sqrt(std::pow(point.x - circle.center.x, 2) + std::pow(point.y - circle.center.y, 2));
    return distance <= circle.radius;
}
void clipPointToCircle(Point& point, const Circle& circle) {    
    if (!isPointInsideCircle(point,circle)) {
        double angle = atan2(point.y - circle.center.y, point.x - circle.center.x);
        point.x = circle.center.x + circle.radius * cos(angle);
        point.y = circle.center.y + circle.radius * sin(angle);
    }
}

int main() {
    Circle circle;
    circle.center.x = 0.0;
    circle.center.y = 0.0;
    circle.radius = 5.0;
    
    Point point;
    point.x = 7.0;
    point.y = 2.0;
    
    cout << "Original point: (" << point.x << ", " << point.y << ")" << std::endl;
    clipPointToCircle(point, circle);
    cout << "Clipped point: (" << point.x << ", " << point.y << ")" << std::endl;
    
    return 0;
}
