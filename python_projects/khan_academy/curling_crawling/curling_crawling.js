// Spiders
// Version 1.0.2
// 6/12/2016
// Robert L. Oelschlaeger

// Create NO_SPIDERS number of spiders in a world containing food, water and a
// moving poison container. As the spiders become thirsty or hungry they have to
// replenish their food and water while avoiding other spiders of other species
// that might like to eat them for their food/water content.

var NO_SPIDERS = 6; // number of spiders
var G = 1; // gravitation constant

// spider color choices
var Colors = [
    color(255, 0, 0, 90),
    color(0, 255, 0, 90),
    color(0, 0, 255, 90),
    color(255, 255, 0, 90),
    color(0, 255, 255, 90),
    color(255, 0, 255, 90)
];

// default mode choices
var reset = function() {
    angleMode = "degrees";
    rectMode(CENTER);
    stroke(0, 0, 0);
    fill(0, 0, 0);
    strokeWeight(1);
};
reset();

////////////////////////////////////////////////////////////////////////
// Spider
////////////////////////////////////////////////////////////////////////

var INITIAL_FOOD = 3000;
var INITIAL_WATER = 3000;

var Spider = function(i, x, y) {
    this.index = i;
    this.position = new PVector(x, y);

    this.acceleration = new PVector(0, 0);
    this.velocity = new PVector(1, -1);

    this.m = random(5, 15); // mass
    this.w = this.m * 4; // width
    this.h = this.m * 2; // height

    this.legAngleDelta = 0;
    this.legAngleRate = random(5, 7);

    this.color = color(255, 0, 0);

    this.alive = true;
    this.water = INITIAL_WATER * random(0.5, 1);
    this.food = INITIAL_FOOD * random(0.5, 1);

    // pick a spider species/color
    this.species = floor(random(Colors.length));
    this.color = Colors[this.species];
};

// return true if spider is alive
Spider.prototype.isAlive = function() {
    return this.alive;
};

// compute and add the acceleration
Spider.prototype.applyForce = function(f) {
    var force = f.get();
    force.div(this.m);
    this.acceleration.add(force);
};

Spider.prototype.draw = function() {

    // if this spider is dead, don't draw anything
    if (this.isAlive() === false) {
        return;
    }

    // find which way it is heading
    var direction = this.velocity.heading();

    strokeWeight(5);

    pushMatrix();

    // translate to center of spider
    translate(this.position.x, this.position.y);

    // rotate to heading
    rotate(direction);

    // red direction indicator
    stroke(255, 0, 0, 90);
    line(0, 0, this.w, 0);

    // show spider number
    fill(255, 255, 255);
    text(this.index, this.w + 10, 4);

    // black legs and body
    stroke(0, 0, 0);
    fill(0, 0, 0);

    // draw the body with rounded corners
    rect(0, 0, this.w, this.h, 80);

    // draw the legs
    for (var leg = 0; leg < 4; leg++) {
        pushMatrix();

        // rhythmic leg variations
        var angle = leg * 40 + 30 + cos(this.legAngleDelta + leg * 30) * 15;

        // first of a leg pair
        rotate(angle);
        line(0, 0, this.w, 0);

        // second of a leg pair
        rotate(-2 * angle);
        line(0, 0, this.w, 0);

        popMatrix();
    }

    // redraw the body the correct color, obscuring the legs in the body
    fill(this.color);
    rect(0, 0, this.w, this.h, 80);

    popMatrix();

    // restore defaults
    reset();

    // adjust the leg speed to the body velocity
    this.legAngleDelta += (this.legAngleRate * this.velocity.mag());

    // check remaining water
    this.water -= 1;
    if (this.water < 0) {
        this.alive = false;
    }

    // check remaining food
    this.food -= 1;
    if (this.food < 0) {
        this.alive = false;
    }
};

// update position
Spider.prototype.update = function() {
    // adjust position from acceleration and velocity
    this.velocity.add(this.acceleration);
    this.velocity.limit(1.0);
    this.position.add(this.velocity);

    // clamp position
    if (this.position.x > 400) {
        this.position.x = 400;
        this.velocity.x = -this.velocity.x;
    } else if (this.position.x < 0) {
        this.position.x = 0;
        this.velocity.x = -this.velocity.x;
    }

    if (this.position.y > 400) {
        this.position.y = 400;
        this.velocity.y = -this.velocity.y;
    } else if (this.position.y < 0) {
        this.position.y = 0;
        this.velocity.y = -this.velocity.y;
    }

    // clear acceleration
    this.acceleration.mult(0);
};

// spiders attract each other
Spider.prototype.attract = function(other) {
    var m1 = this.m;
    var m2 = other.m;
    var r = PVector.dist(this.position, other.position);
    var force = this.position.get();
    force.sub(other.position);
    force.normalize();
    var strength = G * m1 * m2 / (r * r);

    // like-species attract
    if (this.species === other.species) {
        strength = -strength;
        // unless they get too close
        if (r < this.w) {
            strength = -strength;
        }
    }
    force.mult(strength);
    return force;
};

Spider.prototype.battle = function(other) {

    if (other.isAlive() === false) {
        return new PVector(-1, 1);
    }

    var force = this.position.get();
    force.sub(other.position);
    var dist = force.mag();
    force.normalize();
    if (dist > 100) {
        force.mult(-2);
    } else {
        if (this.m > other.m) {
            this.water += 1;
            other.water -= 1;
            // } else if (this.m < other.m) {
            //      other.water += this.water / 2;
            //      this.water /= 2;
            //      other.food += this.food / 2;
            //      this.food /= 2;
        }
    }
    return force;
};

////////////////////////////////////////////////////////////////////////
// Resource
////////////////////////////////////////////////////////////////////////

var Resource = function(x, y, units, text, threshold, capacity, multiplier) {
    this.position = new PVector(x, y);
    this.units = units;
    this.h = 40;
    this.w = 40;
    this.t = text;
    this.threshold = threshold;
    this.capacity = capacity;
    this.multiplier = multiplier;
};

var food = new Resource(100, 100, 1000, "food", 2000, 5000, 9);
var water = new Resource(300, 300, 1000, "water", 2000, 3000, 8);
var poison = new Resource(100, 300, 1000, "poison", 1800, 2400, -10);

Resource.prototype.draw = function() {
    fill(255, 255, 0, 15);
    strokeWeight(4);
    ellipse(this.position.x, this.position.y, this.w, this.h);
    fill(255, 128, 0);
    text(this.t, this.position.x, this.position.y, 100, 100);
    reset();
};

food.computeForce = function(s) {
    // if there already is enough food, no force
    if (s.food > this.threshold) {
        return new PVector(0, 0);
    }

    // compute distance to spider s
    var r = PVector.dist(this.position, s.position);

    // if spider is close enough, it can eat
    if (r < (this.h / 2)) {
        s.food += this.capacity;
    }

    // compute the attractive force
    var force = this.position.get();
    force.sub(s.position);
    force.normalize();
    var mult = this.multiplier * s.m / (r * r);
    if (s.food < 2 * this.capacity) {
        mult *= 5;
    }
    if (s.food < this.capacity) {
        mult *= 5;
    }
    force.mult(mult);
    return force;
};

water.computeForce = function(s) {
    // if there is already enough water, no force
    if (s.water > this.threshold) {
        return new PVector(0, 0);
    }

    // compute the distance to spider s
    var r = PVector.dist(this.position, s.position);

    // if spider is close enough, it can drink
    if (r < (this.h / 2)) {
        s.water += this.capacity;
    }

    // compute the attractive force
    var force = this.position.get();
    force.sub(s.position);
    force.normalize();
    var mult = this.multiplier * s.m / (r * r);
    if (s.water < 2 * this.capacity) {
        mult *= 5;
    }
    if (s.water < this.capacity) {
        mult *= 5;
    }
    force.mult(mult);
    return force;
};

poison.computeForce = function(s) {
    // compute the distance to spider s
    var r = PVector.dist(this.position, s.position);

    // if spider is close enough, it will die
    if (r < (this.h / 2)) {
        s.water = 0;
        s.food = 0;
    }

    // compute the repulsive force
    var force = this.position.get();
    force.sub(s.position);
    force.normalize();
    var mult = this.multiplier * s.m / (r * r);
    force.mult(mult);
    return force;

};

var pCenter = new PVector(200, 200);
var pRadius = 141;
var pAngle = 135;
var pAngleDelta = 0.025;
poison.move = function() {
    var x = pCenter.x + pRadius * cos(pAngle);
    var y = pCenter.x + pRadius * sin(pAngle);
    this.position = new PVector(x, y);
    pAngle += pAngleDelta;
};
poison.move();


////////////////////////////////////////////////////////////////////////

var spiders = [];

for (var i = 0; i < NO_SPIDERS; i++) {
    var x = random(0, 400);
    var y = random(0, 400);
    spiders.push(new Spider(i, x, y));
}

draw = function() {
    background(128, 128, 128);
    text("# food water", 200, 16);

    var living = 0;
    for (var i = 0; i < spiders.length; i++) {
        var spider = spiders[i];
        var force;
        for (var j = 0; j < spiders.length; j++) {
            if (i !== j) {
                // force = new PVector(0.01, -0.01);
                var d = PVector.dist(spider.position, spiders[j].position);
                if (d < 50) {
                    force = spider.battle(spiders[j]);
                } else {
                    force = spider.attract(spiders[j]);
                }
                spider.applyForce(force);
            }
        }

        force = water.computeForce(spider);
        spider.applyForce(force);

        force = food.computeForce(spider);
        spider.applyForce(force);

        force = poison.computeForce(spider);
        spider.applyForce(force);

        food.draw();
        water.draw();
        poison.draw();
        poison.move();

        spider.update();
        spider.draw();

        text(spider.index +
            " " +
            round(spider.food) +
            " " +
            round(spider.water),
            200,
            32 + i * 16
        );
        if (spider.isAlive()) {
            living++;
        } else {
            spiders.splice(i, 1);
        }
    }

    if (living === 0) {
        text("GAME OVER", 200, 200, 400, 400);
    }

};
