library(shiny)
library(dataiku)

shinyServer(function(input, output, session) {
  who_is_running_the_server <- dkuGetAuthInfo()

  who_is_accessing_the_app <- dkuGetAuthInfoFromRookRequest(session$request)

  print(paste("User accessing the app is", who_is_accessing_the_app$authIdentifier))

  if (!"trusted_people" %in% who_is_accessing_the_app$groups) {
    stop("You do not belong here, go away")
  }

  output$whoisserver <- renderText({
    who_is_running_the_server$authIdentifier
  })
  output$whoami <- renderText({
    who_is_accessing_the_app$authIdentifier
  })
})