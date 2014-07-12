import System.IO
import Data.List

main :: IO ()
main = do
    hSetBuffering stdout NoBuffering -- DO NOT REMOVE
    loop

loop :: IO ()
loop = do
    situationInput <- getSituationInput
    outcome <- return (play (readSituation situationInput))
    putStrLn (show outcome)
    loop

getSituationInput :: IO [String]
getSituationInput = sequence (replicate 9 getLine)

readSituation :: [String] -> Situation
readSituation (spaceshipCoordinates:mountainHeights) = (Situation readSpaceship readMountains)
    where
        readSpaceship = Spaceship (Position spaceshipPosition) (Altitude spaceshipAltitude)
        [spaceshipPosition, spaceshipAltitude] = map read (words spaceshipCoordinates)
        readMountains = map readMountain mountainHeightsWithPositions
        readMountain (position, height) = Mountain (Position position) (Height (read height))
        mountainHeightsWithPositions = zip [0..] mountainHeights

data Altitude = Altitude Int deriving (Read, Show, Eq, Ord)
data Height = Height Int deriving (Read, Show, Eq, Ord)
data Position = Position Int deriving (Read, Show, Eq, Ord)
data Spaceship = Spaceship Position Altitude
data Mountain = Mountain {position :: Position, height :: Height} deriving (Eq, Ord)
data Situation = Situation Spaceship [Mountain]
data Outcome = Fire | Hold deriving Show

play :: Situation -> Outcome
play (Situation spaceship mountains) = if spaceship `aboveHighest` mountains then Fire else Hold

aboveHighest :: Spaceship -> [Mountain] -> Bool
aboveHighest (Spaceship position _) mountains = position == (positionOfHighest mountains)

positionOfHighest :: [Mountain] -> Position
positionOfHighest = position . (maximumBy comparingByHeight)
    where comparingByHeight mountainA mountainB = compare (height mountainA) (height mountainB)
