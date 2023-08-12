import datetime
from schema import Schema, And, Use, Optional, SchemaError, Or

robots_2023 = Schema({
    # Robot Info
    "id": And(Use(str)),
    "name": And(Use(str)),
    "weight_kg": And(Use(int)),
    "width_cm": And(Use(int)),
    "height_cm": And(Use(int)),
    "length_cm": And(Use(int)),
    "max_height_cm": And(Use(int)),
    
    # Drivetrain
    "drivetrain_motors": And(Use(int)),
    "drivetrain_type": And(Use(str)),
    
    # Programming
    "language": And(Use(str)),
    "computer_vision": And(Use(bool)),
    "cameras": And(Use(int)),
    "sensors": And(Use([str])),
    "balance": And(Use(bool)),
    "autonomous": And(Use(bool)),
    "auto_mobility": And(Use(bool)),
    "auto_scoring": And(Use(bool)),
    "auto_levels": And(Use([int])),
    "auto_dock": And(Use(bool)),
    "auto_engage": And(Use(bool)),
    "auto_balance": And(Use(bool)),
    "odometry": And(Use(bool)),
    "pathfinding": And(Use(bool)),
    
    # Mechanics
    "intake_pieces": And(Use([str])),
    "intake_type": And(Use(str)),
    "elevator_type": And(Use(str)),
    "arm_type": And(Use(str)),
    "priotity": And(Use([str])),
    "intake_actuators": And(Use(int)),
    "elevator_actuators": And(Use(int)),
    "arm_actuators": And(Use(int)),
    "tele_arm": And(Use(bool)),
    
    # Scouter ratings
    "rating": And(Use(float)),
    "comments": And(Use(str)),
}, ignore_extra_keys=True, name="2023 Robots", description="The schema for the robots from the 2023 season (Charged Up)")

teams_2023 = Schema({
    # Team Info
    "id": And(Use(str)),
    "name": And(Use(str)),
    "matches": And(Use([str])),
    
    # Robot info
    "robot": And(Use(int)),
    
    # Drivers' Info
    "priority": And(Use(int)),
    
    # Scouter ratings
    "rating": And(Use(float)),
    "comments": And(Use(str)),
}, ignore_extra_keys=True, name="2023 Teams", description="The schema for the teams from the 2023 season (Charged Up)")

performances_2023 = Schema({
    # Performance info
    "team": And(Use(str)),
    "robot": And(Use(str)),
    "match": And(Use(str)),
    "start_pos": And(Use(str)),
    
    # Match info
    "level_1": And(Use(int)),
    "level_2": And(Use(int)),
    "level_3": And(Use(int)),
    
    "links": And(Use(int)),
    "pieces": And(Use([str])),
    "end_balance": And(Use(bool)),
    
    "disconnected": And(Use(bool)),
    "disabled": And(Use(bool)),
    "tippyness": And(Use(float)),
    
    # Autonomous info
    "auto_level_1": And(Use(int)),
    "auto_level_2": And(Use(int)),
    "auto_level_3": And(Use(int)),
    
    "auto_balance": And(Use(bool)),
    "auto_pieces": And(Use([str])),
    "auto_mobility": And(Use(bool)),
    
    # Strategy info
    "attack": And(Use(bool)),
    "defense": And(Use(bool)),
    
    # Scouter ratings
    "rating": And(Use(float)),
    "comments": And(Use(str)),
}, ignore_extra_keys=True, name="2023 Performances", description="A performance is created per robot per match. It contains all the information about the robot's performance in that match.")

matches_2023 = Schema({
    "perf_1": And(Use(str)),
    "perf_2": And(Use(str)),
    "perf_3": And(Use(str)),
    "perf_4": And(Use(str)),
    "perf_5": And(Use(str)),
    "perf_6": And(Use(str)),
    "started": And(Use(datetime.datetime)),
    "ended": And(Use(datetime.datetime)),
    "red_pts": And(Use(int)),
    "blue_pts": And(Use(int))
}, ignore_extra_keys=True, name="2023 Matches", description="A match contains a performance per robot, the start and end time and the scores")

schemas = {
    "robots_2023": robots_2023,
    "teams_2023": teams_2023,
    "performances_2023": performances_2023,
    "matches_2023": matches_2023
}