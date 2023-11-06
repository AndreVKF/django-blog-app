
let topicsContainer = document.getElementById("topics_container")
let options = topicsContainer.getElementsByClassName("topic_component__wrapper")

let url = window.location.href
let reQueryParam = /q?=([a-zA-Z0-9_%]*)\/{0,1}/
let queryParam = reQueryParam.exec(url)

if (!queryParam) {
  setSelectedTopic('All')
} else {
  let selectedOption = queryParam[1].replace('%20', ' ')
  setSelectedTopic(selectedOption)
}

function setSelectedTopic(selectedOption) {
  if (!selectedOption) return
  
  let anchorTag, spanTag;

  for (let i = 0; i < options.length; i++) {
    anchorTag = options[i].getElementsByTagName('a')[0]
    spanTag = options[i].getElementsByTagName('span')[0]

    anchorTag.classList.remove('selected_topic')
    spanTag.classList.remove('selected_topic')

    if (anchorTag.text === selectedOption) {
      anchorTag.classList.add('selected_topic')
      spanTag.classList.add('selected_topic')
    }
  }
}