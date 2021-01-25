library(shiny)
library(dataiku)
library(dygraphs)
library(xts)

# Load the data once
df <- dkuReadDataset("bulldozer_full_prepared", samplingMethod="head", nbRows=1000)

shinyServer(function(input, output) {

    output$dygraph <- renderDygraph({
        # Compute the time series with the proper column
        xts_data <- xts(df[input$column], order.by=as.Date(df$saledate_parsed))
        # Compute average by day for the data we plot
        avg <- apply.daily(xts_data, mean)
        
        # And render it
        dygraph(xts_data) %>% dyRangeSelector() %>% dyOptions(drawGrid = input$showgrid)
  }) 
})