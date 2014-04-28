def conway_compress(phrase)
    phrase
        .chunk { |value| value }
        .flat_map { |value, subphrase| [subphrase.length, value] }
end

def conway(root, n)
    n.times.reduce(root) { |phrase| conway_compress(phrase) }
end

if __FILE__ == $0 # main 
    root = [STDIN.gets.to_i]
    n = STDIN.gets.to_i
    nth_conway = conway(root, n - 1)
    puts nth_conway.join(" ")
end
