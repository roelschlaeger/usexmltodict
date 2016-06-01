// ////////////////////////////// //
// Spider and Resources generator //
// Robert Oelschlaeger 5/28/2016  //
// Version: 1.0.0                 //
// ////////////////////////////// //

// default colors
stroke(255, 0, 0);
fill(255, 0, 0);

// Gravitational constant for simulation
var G = 1;

// random number generator
var generator = new Random(1);

// we have these colors with which to distinguish the spider types
var SPECIES_COLOR = [{
    r: 255,
    g: 0,
    b: 0
}, {
    r: 0,
    g: 255,
    b: 0
}, {
    r: 0,
    g: 0,
    b: 255
}, {
    r: 255,
    g: 255,
    b: 0
}, {
    r: 0,
    g: 255,
    b: 255
}, {
    r: 255,
    g: 0,
    b: 255
}, ];

// thus, we have these many species
var NO_OF_SPECIES = SPECIES_COLOR.length * random(0.5, 1);

// the Mover class
var Mover = function(m, x, y) {
    this.mass = m;
    this.position = new PVector(x, y);
    this.velocity = new PVector(0, 0);
    this.acceleration = new PVector(0, 0);

    this.w = m * 10; // width
    this.h = m * 15; // height
    this.hw = max(this.w, this.h); // the larger of height and width
    this.species = floor(random(0, NO_OF_SPECIES)); // pick a species
};

// applyForce
Mover.prototype.applyForce = function(force) {
    var f = PVector.div(force, this.mass);
    this.acceleration.add(f);
};

// Mover.update method
Mover.prototype.update = function() {
    this.acceleration.limit(2);
    this.velocity.add(this.acceleration);
    this.velocity.limit(5);
    this.position.add(this.velocity);
    this.acceleration.mult(0);
};

// Mover.checkedges method
Mover.prototype.checkedges = function() {
    if (this.position.x < this.hw) {
        this.position.x = this.hw;
        // this.acceleration.x = abs(this.acceleration.x);
    } else if (this.position.x > width - this.hw) {
        this.position.x = width - this.hw;
        // this.acceleration.x = -abs(this.acceleration.x);
    }

    if (this.position.y < this.hw) {
        this.position.y = this.hw;
        // this.acceleration.y = abs(this.acceleration.y);
    } else if (this.position.y > (height - this.hw)) {
        this.position.y = (height - this.hw);
        // this.acceleration.y = -abs(this.acceleration.y);
    }
};

Mover.prototype.calculateAttraction = function(m) {
    var force = PVector.sub(this.position, m.position);
    var distance = force.mag();
    distance = constrain(distance, 5.0, 25.0);
    force.normalize();
    var strength = -(G * this.mass * m.mass) / (distance * distance);
    // different species attract each other in this world: think food!
    if (this.species !== m.species) {
        strength = -strength;
        // except that closeness breeds flight: think venom and mandibles!
        if (distance < 25) {
            strength = -2;
        }
    }
    force.mult(strength);
    return force;
};


var t_increment = 0;

Mover.prototype.display = function(index) {

    // some jittering
    var angle = 720 * noise(index, t_increment);
    t_increment += 0.0005;

    // black
    fill(0, 0, 0);

    pushMatrix();

    // select a color based on species
    var rgb = SPECIES_COLOR[this.species];
    stroke(rgb.r, rgb.g, rgb.b);

    // translate the viewport
    translate(this.position.x, this.position.y);
    rotate(angle);

    // adjust for aspect ratio
    if (this.w < this.h) {
        rotate(90);
    }

    pushMatrix();

    // thicklines
    strokeWeight(6);

    // draw legs
    for (var i = 0; i < 4; i++) {
        rotate(35);
        // some jitter on leg length based on location
        if (this.position.x & 32 && this.position.y & 64) {
            line(0, -this.w, 0, this.w);
        } else {
            line(0, -this.w * 0.8, 0, this.w * 0.8);
        }
    }

    popMatrix();

    // draw the body
    ellipse(0, 0, this.w, this.h);

    // draw the eyes
    strokeWeight(4);
    fill(255, 255, 255);
    ellipse(this.w / 6, this.h / 2, this.w / 8, this.w / 4);
    ellipse(-this.w / 6, this.h / 2, this.w / 8, this.w / 4);

    popMatrix();

};

// list of active spiders
var spiders = [];

// the number of spiders for this run
var NUMBER_OF_SPIDERS = NO_OF_SPECIES * random(0.5, 1.5);

// create the spiders
var generate_spiders = function() {
    for (var i = 0; i < NUMBER_OF_SPIDERS; i++) {
        var m = 3 + 1.67 * generator.nextGaussian();
        var x = 200 + 66 * generator.nextGaussian();
        var y = 200 + 33 * generator.nextGaussian();
        spiders.push(new Mover(m, x, y));
    }
};

generate_spiders();

////////////////////////////////////////////////////////////////////////

// for resources that don't move
var FixedResource = function(x, y, w, h, m, t) {
    this.x = x;
    this.y = y;
    this.width = w;
    this.height = h;
    this.mass = m;
    this.text = t;

    this.position = new PVector(x, y);
};

FixedResource.prototype.calculateAttraction = function(m) {
    var force = PVector.sub(this.position, m.position);
    var distance = force.mag();
    // lighter constraint on distance
    distance = constrain(distance, 5.0, 600.0);
    force.normalize();
    var strength = (G * this.mass * m.mass) / (distance * distance);
    force.mult(strength);
    return force;
};

FixedResource.prototype.display = function() {
    fill(62, 181, 43, 64);
    rect(this.x, this.y, this.width, this.height);
    fill(255);
    text(this.text, this.x + 4, this.y + this.height - 6);
};

var food = new FixedResource(360, 360, 40, 40, 10, "Food");
var water = new FixedResource(10, 10, 40, 40, 12, "Water");
var poison = new FixedResource(200, 200, 40, 40, -50, "Poison");

////////////////////////////////////////////////////////////////////////

// main draw function, called periodically by framework
var draw = function() {

    // gray background
    background(128, 128, 128);

    // examine the forces on all of the spiders
    for (var i = 0; i < spiders.length; i++) {

        // the spider on which we are computing the forces
        var theSpider = spiders[i];

        // compute and apply the attraction to food
        var force = food.calculateAttraction(theSpider);
        theSpider.applyForce(force);

        // compute and apply the attraction to water
        force = water.calculateAttraction(theSpider);
        theSpider.applyForce(force);

        // compute and apply the attraction to poison
        force = poison.calculateAttraction(theSpider);
        theSpider.applyForce(force);

        // compute and apply the attraction/repulsion to other spiders
        for (var j = 0; j < spiders.length; j++) {
            if (i !== j) {
                // compute the attraction to spider[j]
                force = spiders[j].calculateAttraction(theSpider);
                // and accumulate it
                theSpider.applyForce(force);
            }
            // with all forces accumulated, perform the update
            theSpider.update();
        }

        // check the range boundaries
        theSpider.checkedges();

        // display the result
        theSpider.display(i);
    }

    // show the food
    food.display();

    // show the water
    water.display();

    // show the poison
    poison.display();

};


