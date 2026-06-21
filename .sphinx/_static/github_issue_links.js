document.addEventListener("DOMContentLoaded", function () {
    var link = document.createElement("a");
    link.classList.add("muted-link", "github-issue-link");
    link.text = "Give feedback";
    link.href = (
        github_url
        + "/issues/new?"
        + "title=docs%3A+TYPE+YOUR+QUESTION+HERE"
        + "&body=*Please describe the question or issue you're facing with "
        + encodeURIComponent('"' + document.title + '"')
        + ".*"
        + "%0A%0A%0A%0A%0A"
        + "---"
        + "%0A"
        + "*Reported+from%3A+" + encodeURIComponent(location.href) + "*"
    );
    link.target = "_blank";

    var div = document.createElement("div");
    div.classList.add("github-issue-link-container");
    div.appendChild(link);

    var container = document.querySelector(".article-container > .content-icon-container");
    if (container) {
        container.prepend(div);
    }
});
