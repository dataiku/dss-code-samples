library(shiny)

shinyUI(fluidPage(
  titlePanel("Hello Shiny!"),
  sidebarLayout(
    # Side bar with "who is running the server"
    sidebarPanel(
      textOutput("whoisserver")
    ),
    mainPanel(
      # Main panel with "who is accessing the app"
      textOutput("whoami")
    )
  )
))