var cols = ["base", "row", "start", "y_value"]
// Estas rutas son fijsa, los archivos se reemplazan al cargar cada nuevo grafo
var arcosPath = "/static/outputs/grafo.csv";
var metadatosPath = "/static/outputs/metadatos.csv"
// Colores que establecemos para que quede más visual, si no los estaleciéramos se quedarían los de por defecto
var colores_secuencias = ["#F1A99A", "#F9D566", "#7ED8BB", "#7EC4D8", "#D87E89", "#ECB4F4", "#BCF4EE", "#F0F4BC", "#C0F0B1", "#89F3C9"]
var colores_arcos = ['#FFC0CB', '#87CEEB ', '#FFE4E1', '#B3F389', '#FFDAB9', '#BA55D3', '#ECF389', '#AFEEEE', '#89A1F3'];
// Valores para los arcos, dependiendo del valor tienen un color diferente los arcos
var valores_cigar = ["Match", "Insertion",  "Deletion" ,"Skipped region ", "Soft clipping", "Hard clipping ","Padding"]
function createGraph(intervalo_ini, secuencias, output, screenWidth, screenHeight) {
  zoom_ini_rect = intervalo_ini.slice();
  zoom_ini_rect[1] = intervalo_ini[0]+200

  var my_graph = {
      "arrangement": "vertical",
      "assembly": "unknown",
      "views": [
        {
        "spacing": 40,
        "arrangement": "horizontal",
        "views":[
          {
            "layout": "circular",
            "xDomain": {"interval": intervalo_ini},
            "tracks": [
              {
                "alignment": "overlay",
                "data": {
                  "url": output,
                  "type": "csv",
                  "genomicFields": cols
                },
                "x": {"field": "start", "type": "genomic"},
                "color": {
                  "field": "row",
                  "type": "nominal",
                  "legend": true,
                  "domain": secuencias,
                  "range": colores_secuencias
                },
                "text": {"field": "base", "type": "nominal"},
                "style": {"textFontWeight": "bold"},
                "width": screenWidth * 0.38, // Radio del grafo
                "height": screenHeight * 0.5, // Ancho de la banda
                "row": {"field": "row", "type": "nominal"},
                "tracks": [
                  {
                    "mark": "bar",
                    "y": {"field": "y_value", "type": "quantitative", "axis": "none"}
                  },
                  {
                    "dataTransform": [
                      {"type": "filter", "field": "count", "oneOf": [0], "not": true}
                    ],
                    "mark": "text",
                    "size": {"value": 24},
                    "color": {"value": "white"},
                    "visibility": [
                      {
                        "operation": "less-than",
                        "measure": "width",
                        "threshold": "|xe-x|",
                        "transitionPadding": 0,
                        "target": "mark"
                      },
                      {
                        "operation": "LT",
                        "measure": "zoomLevel",
                        "threshold": 40,
                        "target": "track"
                      }
                    ]
                  },
                  {
                    "mark": "brush",
                    "x": {"linkingId": "detail-1"},
                    "color": {"value": "blue"}
                  }
                ]
              },
              {
                "data": {
                  "url": arcosPath,
                  "type": "csv",
                  "genomicFields": ["start", "end"]
                },
                "mark": "withinLink",
                "x": {"field": "start", "type": "genomic"},
                "xe": {"field": "end", "type": "genomic"},
                "stroke": {"field": "overlap", "type": "nominal", "range": colores_arcos},
                "strokeWidth": {"value": 1},
                "opacity": {"value": 0.6},
                "color": {
                  "field": "overlap",
                  "type": "nominal",
                  "legend": false,
                  "domain": valores_cigar, 
                  "range": colores_arcos
                }
              },
              {
                "data": {
                  "url": metadatosPath,
                  "type": "csv",
                  "genomicFields": ["gen", "start", "end"]
                },
                "text": {"field": "gen", "type": "nominal"},
                "mark": "text",
                "x": {"field": "start", "type": "genomic"},
                "xe": {"field": "end", "type": "genomic"}
              }
            ]
          },
          {
            "linkingId": "detail-1",
            "layout": "linear",
            "xDomain": {"interval": zoom_ini_rect},
            "tracks": [
              {
                "style": {"outline": "#8DC1F2", "outlineWidth": 2},
                "alignment": "overlay",
                "data": {
                  "url": output,
                  "type": "csv",
                  "genomicFields": cols
                },
                "x": {"field": "start", "type": "genomic"},
                "color": {
                  "field": "row",
                  "type": "nominal",
                  "legend": false,
                  "domain": secuencias, 
                  "range": colores_secuencias
                },
                "text": {"field": "base", "type": "nominal"},
                "width": screenWidth * 0.28, // ancho rectangulo metadatos
                "height": screenHeight * 0.20, // alta rectangulo metadatos
                "row": {"field": "row", "type": "nominal"},
                "tracks": [
                  {
                    "mark": "bar",
                    "y": {"field": "y_value", "type": "quantitative", "axis": "none"}
                  },
                  {
                    "dataTransform": [
                      {"type": "filter", "field": "count", "oneOf": [0], "not": true}
                    ],
                    "mark": "text",
                    "size": {"value": 24},
                    "color": {"value": "white"},
                    "visibility": [
                      {
                        "operation": "less-than",
                        "measure": "width",
                        "threshold": "|xe-x|",
                        "transitionPadding": 0,
                        "target": "mark"
                      },
                      {
                        "operation": "LT",
                        "measure": "zoomLevel",
                        "threshold": 40,
                        "target": "track"
                      }
                    ]
                  }
                ]
              },
              {
                "style": {"outline": "#8DC1F2", "outlineWidth": 2},
                "data": {
                  "url": arcosPath,
                  "type": "csv",
                  "genomicFields": ["start", "end"]
                },
                "mark": "withinLink",
                "x": {"field": "start", "type": "genomic"},
                "xe": {"field": "end", "type": "genomic"},
                "stroke": {"field": "overlap", "type": "nominal", "range": colores_arcos},
                "strokeWidth": {"value": 1},
                "opacity": {"value": 0.6},
                "width": screenWidth * 0.065, // dimensiones rectángulo inferior letras
                "height": screenHeight * 0.5,
                "color": {
                  "field": "overlap",
                  "type": "nominal",
                  "legend": true,
                  "domain": valores_cigar, 
                  "range": colores_arcos
                }
              }
            ]
          }    
        ]
        }
      ]
  }
  return my_graph;
}

function getMetadata(nombreGen){ 
  var ruta = "/static/outputs/metadatos.csv";
  $.ajax({
    url: ruta,
    dataType: "text",
    success: function(datos) {
      var filas = datos.split("\n").map(function(linea) {
        return linea.split(",");
      });
      for (var i = 1; i < filas.length; i++) {
        if (filas[i][0] == nombreGen) {
          var metadata = {
            gen: filas[i][0],
            start: filas[i][1],
            end: filas[i][2],
            id: filas[i][3],
            locus_tag: filas[i][4],
            type: filas[i][5]
          };
          let metadataInfo = $('#metadataInfo');
          metadataInfo.html('<strong>Gen:</strong> ' + metadata.gen + '&nbsp;&nbsp;&nbsp;&nbsp;<strong>Start:</strong> ' + metadata.start + '&nbsp;&nbsp;&nbsp;&nbsp;<strong>End:</strong> ' +
           metadata.end + '&nbsp;&nbsp;&nbsp;&nbsp;<strong>Id:</strong> ' + metadata.id + '&nbsp;&nbsp;&nbsp;&nbsp;<strong>Locus_tag:</strong> ' + metadata.locus_tag  + '&nbsp;&nbsp;&nbsp;&nbsp;<strong>Strand:</strong> ' +
            metadata.type);
          break;
        }
      }
    }
  });
}
