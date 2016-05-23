const letterWidth = parseInt(readline())
const letterHeight = parseInt(readline())
const text = readline()
const letters = times(letterHeight, readline)
    .map(line => chunks(line, letterWidth))

const artLetters = text.split('').map(letter => {
    let index = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".indexOf(letter.toUpperCase())
    if (index < 0) index = 26
    return letters.map(line => line[index])
})

const lines = times(letterHeight, i => {
    return artLetters.map(line => line[i]).join("")
})

print(lines.join("\n"))


function times(n, f) {
    return Array(n).fill(0).map((_, i) => f(i))
}

function chunks(str, n) {
    return str.split('').reduce((chunks, x, i) => {
        if (i % n === 0) chunks.push('')
        chunks[chunks.length - 1] += x
        return chunks
    }, [])
}
