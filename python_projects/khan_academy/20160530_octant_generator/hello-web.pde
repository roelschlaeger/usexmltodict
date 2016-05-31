// vim:ts=4:sw=4:tw=0:wm=0:et:ft=javascript
var position = new PVector(200, 200);
var velocity = new PVector(1, 2);

void draw() {
    background(100);

    fill(255, 255, 255);
    stroke(0, 0, 255);

    noFill();
    rect(0, 0, width-1, height-1);
    fill(255, 0, 0);

    fill(255, 0, 0);
    ellipse(position.x, position.y, 25, 25);

    var angle = atan2(velocity.y, velocity.x);
    var m = velocity.mag() * 20;

    pushMatrix();
        translate(position.x, position.y);
        rotate(angle);
        strokeWeight(4);
        line(0, 0, m, m);
    popMatrix();

    var x = position.x;
    var y = position.y;
    if (x < 0) {
        if (velocity.x < 0) {
            velocity.x = -(velocity.x * random(0.5, 1.2));
            println(velocity.x);
        }
    } else if (x > width) {
        if (velocity.x > 0) {
            velocity.x = -(velocity.x * random(0.5, 1.2));
            println(velocity.x);
        }
    }
    if (y < 0) {
        if (velocity.y < 0) {
            velocity.y = -(velocity.y * random(0.5, 1.2));
            println(velocity.y);
        }
    } else if (y > height) {
        if (velocity.y > 0) {
            velocity.y = -(velocity.y * random(0.5, 1.2));
            println(velocity.y);
        }
    }
    velocity.limit(3);
    position.add(velocity);
}

void setup() {
    ellipseMode(EDGE);
    size(400, 400);
    background(100);
    stroke(255);
    println("hello web!");
    // draw();
}
