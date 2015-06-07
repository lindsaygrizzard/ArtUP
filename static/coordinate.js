
//RESTORE ART FLOATS
function restoreArtFloats(art){
    for(var i=0; i<art.length; i++){
        art[i].art_width = art[i].art_width / 1000 * delta;
        art[i].art_height =art[i].art_height / 1000 * delta;
        art[i].device_distance = art[i].device_distance / 1000 * delta;
    }
}

// FIND TOTAL WIDTH OF ART
function allArtsWidths(obj){
    for ( var w = 0; w < obj.length; w++ ){
        totArtWidth += obj[w].art_width;
    }
}

// MIDDLE AND END MARGINS
function Margins() {
    blankWall = wall.wall_width - totArtWidth ;
    consistantMargins = (blankWall / (art.length + 1));
    offset = consistantMargins * wall.offset_percent;
    midMargin = consistantMargins - offset;
    if (art.length === 2) {
        endMargin = consistantMargins + offset / 2;
    } else if (art.length === 1){
        endMargin = consistantMargins;
        midMargin = 0;
    } else {
        endMargin = consistantMargins + offset;
    }
}

// UPPER EDGE LONGITUDE OF ALL ARTS
function upperX(obj) {
    for(var i = 0; i < obj.length; i ++){
        var each = obj[i].art_height / 2 + wall.center_line;
        obj[i].upperEdge = each;
    }
}

//LEFT CORNER COORDINATES FOR MAPPING
function leftCornerCords(obj){
    p0 = endMargin;
    p = midMargin;
    xAxis = [p0];
    for(i=1; i<obj.length; i++){
        xAxis[i] = xAxis[i-1] + obj[i-1].art_width + p;
    }
    for(var i = 0; i < xAxis.length; i++){
        obj[i].leftCorner = {X : 0};
        obj[i].leftCorner.X = xAxis[i];
    }
}

//"SCREW/TAC POINT" FOR USER INFO
function findPegPoint(obj){
    for(var i = 0; i < obj.length; i++){
        obj[i].leftCorner.Y = obj[i].upperEdge;
        obj[i].leftCorner.Y = Math.round(obj[i].leftCorner.Y * 100) / 100;
        obj[i].leftCorner.X = Math.round(obj[i].leftCorner.X * 100) / 100;

        if (obj[i].device_code === 'none'){
            obj[i].pegPoint = {X : obj[i].leftCorner.X,
                                    Y : obj[i].leftCorner.Y};
        } else {
            obj[i].pegPoint = {X : (obj[i].leftCorner.X +
                                    obj[i].art_width/2),
                                  Y : (obj[i].leftCorner.Y -
                                    obj[i].device_distance)};
            
        }
    }
}

//ORIGINAL CALCULATION DATA
function originalOutput(){
    for(i=0; i<art.length; i++) {
         //Find X origin coord
        var XO = document.getElementById(art[i].art_id+"_OX");
            if(art[i].device_code === "none"){
                    decimal = Math.round(art[i].leftCorner.X) / delta;
                    temp = decimal * 8;
                    roundTemp = Math.ceil(temp);
                    output = roundTemp/8;
                    XO.innerHTML = fraction(output) +" in";

             } else {
                    decimal = Math.round(art[i].leftCorner.X + art[i].art_width/2) / delta;
                    temp = decimal * 8;
                    roundTemp = Math.ceil(temp);
                    output = roundTemp/8;
                    XO.innerHTML = fraction(output) +" in";
             }
         //Find Y origin ccoord
         var YO = document.getElementById(art[i].art_id+"_OY");
             if(art[i].device_code === "none") {
                        decimal= Math.round(art[i].leftCorner.Y) / delta ;
                        temp = decimal * 8;
                        roundTemp = Math.ceil(temp);
                        output = roundTemp/8;
                        YO.innerHTML = fraction(output) +" in";
             } else {
                        decimal = Math.round(art[i].leftCorner.Y - art[i].device_distance) / delta;
                        temp = decimal * 8;
                        roundTemp = Math.ceil(temp);
                        output = roundTemp/8;
                        YO.innerHTML = fraction(output) +" in";
             }
        //tell user device type
        var device = document.getElementById(art[i].art_id+"_D");
                if(art[i].device_code === "none") {
                    device.innerHTML = "Use Left Corner";
            } else {
                device.innerHTML = "Wire";
            }
    }
    //Original Margins    
    var endMarginOrigin = document.getElementById("EMO");
        decimal = Math.round(endMargin) / delta;
        temp = decimal * 8;
        roundTemp = Math.ceil(temp);
        output = roundTemp/8;
        endMarginOrigin.innerHTML = fraction(output) +" in";

    var midMarginOrigin = document.getElementById("MMO");
        decimal = Math.round(midMargin) / delta;
        temp = decimal * 8;
        roundTemp = Math.ceil(temp);
        output = roundTemp/8;
        midMarginOrigin.innerHTML = fraction(output);
        if (art.length === 1) { 
            $("#mid-margin").hide();
            $("#MMO").hide();
        }
}

//D3 RENDER IMAGES AND BACKGROUND RECTANGLES
function dynamicRectangles(){
    var drag = d3.behavior.drag()
        .on("drag", dragMove);

    var svg = d3.select(".wall")
                        .append("svg")
                        .attr("width", wall.wall_width)
                        .attr("height", wall.wall_height)
                        .attr("class", "bgimage")
                        .style("border", "1px dashed black");
                        
    var rect = svg.selectAll(".draggableRectangle").data(art).enter()
            .append('image')
            .attr('class', 'draggableRectangle')
            .attr('name', function(d) { return d.art_name; })
            .attr('device', function(d) { return d.device_code; })
            .attr('x', function(d) { return d.leftCorner.X; })
            .attr('y', function(d) {return wall.wall_height - d.leftCorner.Y; })
            .attr('Ox', function(d) { return d.leftCorner.X; })
            .attr('Oy', function(d) {return wall.wall_height - d.leftCorner.Y; })
            .attr('width', function(d) { return d.art_width; })
            .attr('height', function(d) { return d.art_height; })
            .attr("xlink:href", function(d) { return d.art_img; })
            .attr("style", "outline: 1px solid rgba(0,0,0,0.1);")
            .call(drag);

    var line = svg.append("line")
                .attr("x1", wall.wall_width/2)
                .attr("y1", wall.wall_height)
                .attr("x2", wall.wall_width/2)
                .attr("y2", 0)
                .attr("stroke-width", 2)
                .attr("stroke", "rgba(255,0,0,0.1)");

    line = svg.append("line")
                .attr("x1", 0)
                .attr("y1", wall.wall_height - wall.center_line)
                .attr("x2", wall.wall_width)
                .attr("y2", wall.wall_height - wall.center_line)
                .attr("stroke-width", 2)
                .attr("stroke", "rgba(255,0,0,0.1)");


    function dragMove(d) {
        //if art has hanging wire, math it in. Else return top left corner
             d3.select(this)
                 .attr("x", function () {return d3.event.x;})
                 .attr("y", function () {return d3.event.y;});

             var name = document.getElementById(d.art_name);
                     name.innerHTML = d.art_name;

             var image = d3.selectAll("image");

             //smallest x cord (to find most left art work)
             var minXValue = d3.min(image[0], function(d) {
               return d.x.animVal.value; }) //returns smallest x value
             var leftEndMargin = document.getElementById("LEM");
                leftEndMargin.innerHTML = Math.round(minXValue / delta)+" in";

             //largest x cord (to find most right art work)
             var maxXValue = d3.max(image[0], function(d) {
               return d.x.animVal.value + d.width.animVal.value; });
             var rightEndMargin = document.getElementById("REM");
                rightEndMargin.innerHTML = Math.round((wall.wall_width - maxXValue) / delta)+" in";


             if(d.device_code === "none"){
                    var X = document.getElementById(d.art_id+"_X");
                        X.innerHTML = Math.round(d3.event.x / delta);
             } else {
                    var X = document.getElementById(d.art_id+"_X");
                        X.innerHTML = Math.round((d3.event.x + d.art_width/2) / delta)+" in";
             }
             if(d.device_code === "none") {
                    var Y = document.getElementById(d.art_id+"_Y");
                        Y.innerHTML = Math.round((wall.wall_height -d3.event.y)/ delta)+" in";
             } else {
                    var Y = document.getElementById(d.art_id+"_Y");
                        Y.innerHTML = Math.round(((wall.wall_height -d3.event.y) -
                                                                    d.device_distance)/ delta)+" in";
             }
     }
}

