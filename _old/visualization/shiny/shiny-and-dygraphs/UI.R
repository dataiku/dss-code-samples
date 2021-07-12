library(shiny)
library(dygraphs)

shinyUI(fluidPage(

  titlePanel("Showing time series"),

  sidebarLayout(
    # Sidebar with column selector and "show grid" option"
    sidebarPanel(
      selectInput("column", "Column",
             c("SalePrice", "MachineHoursCurrentMeter", "MachineID")),
      checkboxInput("showgrid", label = "Show Grid", value = TRUE)
    ),

    # Main panel shows the graph itself
    mainPanel(
       dygraphOutput("dygraph")
    )
  )
))