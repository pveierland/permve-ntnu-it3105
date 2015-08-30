require.config({
    paths: {
        d3: "http://d3js.org/d3.v3.min"
    }
});

define([
    "nbextensions/widgets/widgets/js/widget",
    "d3"
], function(widget, d3) {
    var NavigationGridView = widget.DOMWidgetView.extend({  
        render: function() {
            var svg = $('<svg height="' + this.model.get('screen_size').x + '" width="' + this.model.get('screen_size').y + '" />');
            this.setElement(svg);
            
            var gridCellSize = this.model.get('grid_cell_size');
            var gridSize = this.model.get('grid_size');

            this.svgSize = { width: gridSize.x * gridCellSize, height: gridSize.y * gridCellSize };

            var xScale = d3.scale.linear().domain([0,gridSize.x]).range([0,this.svgSize.width]);
            var yScale = d3.scale.linear().domain([0,gridSize.y]).range([0,this.svgSize.height]);

            var scales = { x: xScale, y: yScale };
            var container = this.$el;

            console.log("WAT UP");
            console.log(this.model.get('grid_colors'));

            var cells = d3.select(this.el).selectAll("rect")
                                 .data(this.model.get('grid_colors'))
                                 .enter()
                                 .append("rect")
                                 .attr("x", function (d, i) { return scales.x((i % gridSize.x)); })
                                 .attr("y", function (d, i) { return scales.y(gridSize.y - Math.floor(i / gridSize.x) - 1); })
                                 .attr("width", function (d) { return gridCellSize; })
                                 .attr("height", function (d) { return gridCellSize; });

            this.update();
        },

        update: function() {
            console.log("MOFO MOFO MOFO");
            var gridCellSize = this.model.get('grid_cell_size');
            var gridSize = this.model.get('grid_size');

            this.svgSize = { width: gridSize.x * gridCellSize, height: gridSize.y * gridCellSize };

            var xScale = d3.scale.linear().domain([0,gridSize.x]).range([0,this.svgSize.width]);
            var yScale = d3.scale.linear().domain([0,gridSize.y]).range([0,this.svgSize.height]);

            var scales = { x: xScale, y: yScale };
            var container = this.$el;

            var cells = d3.select(this.el).selectAll("rect")
                                 .data(this.model.get('grid_colors'))
                                 .attr("style", function(d, i) { return "fill: " + d });

            return NavigationGridView.__super__.update.apply(this);
        },
    });

    return {
        'NavigationGridView': NavigationGridView
    };
});
