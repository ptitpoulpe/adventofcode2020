
parse :: String -> [Int]
parse content = do
   let linesOfFiles = lines content
   map read linesOfFiles

partOne :: [Int] -> Int
partOne numbers = do
    let n = head (filter (\x -> 2020 - x `elem` numbers) numbers)
    n * (2020 - n)

partTwo :: [Int] -> Int
partTwo numbers = do
    let l = iterate combine [(0,1)] !! 3
    snd $ head $ filter (\x -> fst x == 2020) l
    where combine computed = 
            [(sv, m * v) | (s, m) <- computed,
                           v <- numbers,
                           let sv = s + v,
                           sv <= 2020]

main :: IO ()
main = do
    contents <- readFile "input"
    let numbers = parse contents
    putStrLn $ "PartOne: " ++ show (partOne numbers)
    putStrLn $ "PartTwo: " ++ show (partTwo numbers)
