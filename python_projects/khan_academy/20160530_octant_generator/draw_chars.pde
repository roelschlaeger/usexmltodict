// vim:ts=4:sw=4:tw=0:wm=0:et:ft=javascript
var symbols = [];

void fill_symbols() {
    for (var i = 0; i < 4; i++) {
        for (var j = 0; j < 4; j++) {
            symbols.push([i, j]);
        }
    }
}

var ARM_LENGTH = 10;
var ARM_SPACING = 3 * ARM_LENGTH + 5;
var ARM_X_MIN = ARM_SPACING;
var ARM_Y_MIN = ARM_SPACING;
var ARM_X = ARM_X_MIN;
var ARM_Y = ARM_Y_MIN;

void adjust_symbol_location() {
    ARM_X += ARM_SPACING;
    if (ARM_X > width) {
        ARM_X = ARM_X_MIN;
        ARM_Y += ARM_SPACING;
    }
    if (ARM_Y > height) {
        ARM_Y = ARM_Y_MIN;
    }
}

void reset_symbol_location() {
    ARM_X = ARM_X_MIN;
    ARM_Y - ARM_Y_MIN;
}

void draw_symbol(a, b) {
    pushMatrix();

        translate(ARM_X, ARM_Y);
        ellipse(0, 0, 5, 5);

        pushMatrix();
            rotate(a * HALF_PI);
            line(0, 0, ARM_LENGTH, ARM_LENGTH);
        popMatrix();

        rotate(b * HALF_PI + 3 * HALF_PI/2);
        line(0, 0, ARM_LENGTH, ARM_LENGTH);

    popMatrix();
    adjust_symbol_location();
}

void draw_symbols() {
    reset_symbol_location();
    text(ARM_Y, 10, 10);
    for (var i = 0; i < symbols.length; i++) {
        var symbol = symbols[i];
        draw_symbol(symbol[0], symbol[1]);
    }
}

void draw() {
    background(100);

    fill(255, 255, 255);
    stroke(0, 0, 255);

    noFill();
    rect(0, 0, width-1, height-1);

    fill(255, 0, 0);
    strokeWeight(2);
    ellipse(200, 200, 100, 100);

    draw_symbols();

}

void setup() {
    ellipseMode(EDGE);
    size(400, 400);
    background(100);
    stroke(255);
    fill_symbols();
    println("hello web!");
}
