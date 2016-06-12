var NO_SPIDERS = 8;
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

var INITIAL_FOOD = 2400;
var INITIAL_WATER = 2400;

var Spider = function(x, y) {
    this.acceleration = new PVector(0, 0);
    this.velocity = new PVector(1, -1);
    this.position = new PVector(x, y);
    this.m = random(5, 15);
    this.w = this.m * 4;
    this.h = this.m * 2;
    this.legAngleDelta = 0;
    this.legAngleRate = random(5, 6);
    this.color = color(255, 0, 0);
    this.water = INITIAL_WATER * random(0.5, 1);
    this.food = INITIAL_FOOD * random(0.5, 1);
    this.alive = true;
    this.species = floor(random(Colors.length));
    this.color = Colors[this.species];
};

Spider.prototype.isAlive = function() {
    return this.alive;
};

Spider.prototype.applyForce = function(f) {
    var force = f.get();
    force.div(this.m);
    this.acceleration.add(force);
};

Spider.prototype.draw = function() {

    if (this.isAlive() === false) {
        return;
    }

    var direction = this.velocity.heading();

    // noFill();
    strokeWeight(5);
    pushMatrix();
    translate(this.position.x, this.position.y);
    rotate(direction);
    line(0, 0, this.w, 0);
    fill(0, 0, 0);
    rect(0, 0, this.w, this.h, 80);
    fill(255, 0, 0);
    for (var leg = 0; leg < 4; leg++) {
        pushMatrix();
        var angle = leg * 40 + 30 + cos(this.legAngleDelta) * 15;
        rotate(angle);
        line(0, 0, this.w, 0);
        rotate(-2 * angle);
        line(0, 0, this.w, 0);
        popMatrix();
    }
    fill(this.color);
    rect(0, 0, this.w, this.h, 80);
    popMatrix();
    reset();

    this.legAngleDelta += (this.legAngleRate * this.velocity.mag());

    this.water -= 1;
    if (this.water < 0) {
        this.alive = false;
    }

    this.food -= 1;
    if (this.food < 0) {
        this.alive = false;
    }
};

Spider.prototype.update = function() {
    this.velocity.add(this.acceleration);
    this.velocity.limit(0.5);
    this.position.add(this.velocity);

    if (this.position.x > 400) {
        this.position.x = 400;
    } else if (this.position.x < 0) {
        this.position.x = 0;
    }

    if (this.position.y > 400) {
        this.position.y = 400;
    } else if (this.position.y < 0) {
        this.position.y = 0;
    }

    // clear acceleration
    this.acceleration.mult(0);
};

Spider.prototype.attract = function(other) {
    var m1 = this.m;
    var m2 = other.m;
    var r = PVector.dist(this.position, other.position);
    var force = this.position.get();
    force.sub(other.position);
    force.normalize();
    var strength = G * m1 * m2 / (r * r);
    if (this.species === other.species) {
        strength = -strength;
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

var food = new Resource(100, 100, 1000, "food", 1800, 4800, 10);
var water = new Resource(300, 300, 1000, "water", 1800, 2400, 1);
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
    force.mult(this.multiplier);
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
    force.mult(this.multiplier);
    return force;
};

poison.computeForce = function(s) {
//  // if there is already enough water, no force
//  if (s.water > this.threshold) {
//      return new PVector(0, 0);
//  }

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
    force.mult(this.multiplier);
    return force;

}////////////////////////////////////////////////////////////////////////

var spiders = [];

for (var i = 0; i < NO_SPIDERS; i++) {
    var x = random(0, 400);
    var y = random(0, 400);
    spiders.push(new Spider(x, y));
}

draw = function() {
    background(128, 128, 128);
    var living = 0;
    for (var i = 0; i < spiders.length; i++) {
        var spider = spiders[i];
        var force;
        for (var j = 0; j < spiders.length; j++) {
            if (i !== j) {
                force = new PVector(0.01, -0.01);
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

        spider.update();
        spider.draw();
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
