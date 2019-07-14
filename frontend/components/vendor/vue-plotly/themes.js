import defaultsDeep from "lodash/defaultsDeep"

const lightLayout = layout =>
    defaultsDeep(layout, {
        font: {
            family: "Roboto, sans-serif"
        },

        plot_bgcolor: "#FFF",
        paper_bgcolor: "#FFF",

        titlefont: {
            size: 16,
            color: "#757575"
        },

        colorway: [
            "#4285F4",
            "#DB4437",
            "#F4B400",
            "#3F51B5",
            "#E91E63",
            "#9C27B0",
            "#673AB7",
            "#F44336",
            "#2196F3",
            "#03A9F4",
            "#00BCD4",
            "#009688"
        ],

        xaxis: {
            rangeslider: {
                visible: false,
                borderwidth: 0
            },

            zerolinecolor: "#9E9E9E",

            gridcolor: "#E0E0E0",

            titlefont: {
                color: "#424242",
                size: 12
            },

            tickfont: {
                color: "#757575",
                size: 12
            },

            showgrid: false
        },

        yaxis: {
            zerolinecolor: "#9E9E9E",

            gridcolor: "#E0E0E0",

            titlefont: {
                color: "#424242",
                size: 12
            },

            tickfont: {
                color: "#757575",
                size: 12
            }
        },

        yaxis2: {
            zerolinecolor: "#9E9E9E",

            gridcolor: "#E0E0E0",

            titlefont: {
                color: "#424242",
                size: 12
            },

            tickfont: {
                color: "#757575",
                size: 12
            }
        },

        polar: {
            radialaxis: {
                showticklabels: false,
                gridcolor: "#E0E0E0",
                ticks: "",
                linewidth: 0
            },

            angularaxis: {
                tickcolor: "#B4B4B4",
                linecolor: "#E0E0E0"
            }
        },

        scene: {
            xaxis: {
                spikecolor: "#E0E0E0"
            },

            yaxis: {
                spikecolor: "#E0E0E0"
            },

            zaxis: {
                spikecolor: "#E0E0E0"
            }
        },

        geo: {
            rivercolor: "#A2D6FF",
            lakecolor: "#A2D6FF",
            showocean: true,
            oceancolor: "#A2D6FF",
            showcountries: true,
            landcolor: "#EDEBE7",
            countrycolor: "#D3D3D3",
            coastlinewidth: 0.5,
            coastlinecolor: "#B4B4B4",
            showframe: false,
            projection: {
                type: "mercator"
            }
        },

        ternary: {
            aaxis: {
                color: "#9E9E9E",
                gridcolor: "#E0E0E0"
            },

            baxis: {
                color: "#9E9E9E",
                gridcolor: "#E0E0E0"
            },

            caxis: {
                color: "#9E9E9E",
                gridcolor: "#E0E0E0"
            }
        },

        bargroupgap: 0.02,

        legend: {
            font: {
                size: 16,
                color: "#757575"
            }
        }
    })

const darkLayout = layout =>
    defaultsDeep(layout, {
        font: {
            family: "Roboto, sans-serif"
        },

        plot_bgcolor: "#424242",
        paper_bgcolor: "#424242",

        titlefont: {
            size: 16,
            color: "#D2D1D1"
        },

        colorway: [
            "#4285F4",
            "#DB4437",
            "#F4B400",
            "#3F51B5",
            "#E91E63",
            "#9C27B0",
            "#673AB7",
            "#F44336",
            "#2196F3",
            "#03A9F4",
            "#00BCD4",
            "#009688"
        ],

        xaxis: {
            rangeslider: {
                visible: false,
                borderwidth: 0
            },

            zerolinecolor: "#FEFEFE",

            gridcolor: "#878686",

            titlefont: {
                color: "#A8A6A6",
                size: 12
            },

            tickfont: {
                color: "#D2D1D1",
                size: 12
            },

            showgrid: false
        },

        yaxis: {
            zerolinecolor: "#FEFEFE",

            gridcolor: "#878686",

            titlefont: {
                color: "#A8A6A6",
                size: 12
            },

            tickfont: {
                color: "#D2D1D1",
                size: 12
            }
        },

        yaxis2: {
            zerolinecolor: "#FEFEFE",

            gridcolor: "#878686",

            titlefont: {
                color: "#A8A6A6",
                size: 12
            },

            tickfont: {
                color: "#D2D1D1",
                size: 12
            }
        },

        polar: {
            radialaxis: {
                showticklabels: false,
                gridcolor: "#878686",
                ticks: "",
                linewidth: 0
            },

            angularaxis: {
                tickcolor: "#B4B4B4",
                linecolor: "#878686"
            }
        },

        scene: {
            xaxis: {
                spikecolor: "#878686"
            },

            yaxis: {
                spikecolor: "#878686"
            },

            zaxis: {
                spikecolor: "#878686"
            }
        },

        geo: {
            rivercolor: "#A2D6FF",
            lakecolor: "#A2D6FF",
            showocean: true,
            oceancolor: "#A2D6FF",
            showcountries: true,
            landcolor: "#EDEBE7",
            countrycolor: "#D3D3D3",
            coastlinewidth: 0.5,
            coastlinecolor: "#B4B4B4",
            showframe: false,
            projection: {
                type: "mercator"
            }
        },

        ternary: {
            aaxis: {
                color: "#FEFEFE",
                gridcolor: "#878686"
            },

            baxis: {
                color: "#FEFEFE",
                gridcolor: "#878686"
            },

            caxis: {
                color: "#FEFEFE",
                gridcolor: "#878686"
            }
        },

        bargroupgap: 0.02,

        legend: {
            font: {
                size: 16,
                color: "#D2D1D1"
            }
        }
    })

export {
    lightLayout,
    darkLayout
}
