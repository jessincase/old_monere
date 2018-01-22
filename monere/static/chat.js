function find_username(username) {
    var position = username.search("username")+11;
    var end_position = username.indexOf('"', position);

    return username.substring(position, end_position);
}

$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    //var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);

    $("#chatform").on("submit", function(event) {
        var message = {
            user: $('#user').val(),
            message: $('#message').val(),
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });

    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var chat = $("#chat")
        var ele = $('<tr></tr>')


        ele.append(
            $("<td></td>").text(data.timestamp)
        )
        ele.append(
            $("<td></td>").text(find_username(JSON.stringify(data.user)))
        )
        ele.append(
            $("<td></td>").text(data.message)
        )

        chat.append(ele)

    };
});

