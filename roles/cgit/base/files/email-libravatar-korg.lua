local md5 = require("md5")

function filter_open(email, page)
        buffer = ""
        hexdigest = md5.sumhexa(email:sub(2, -2):lower())
end

function filter_close()
        html("<span class='libravatar'><img class='inline' src='https://seccdn.libravatar.org/avatar/" .. hexdigest ..  "?s=20&amp;d=retro' /><img class='onhover' src='https://seccdn.libravatar.org/avatar/" .. hexdigest ..  "?s=128&amp;d=retro' /></span>" .. buffer)
        return 0
end

function filter_write(str)
        buffer = buffer .. str
end
