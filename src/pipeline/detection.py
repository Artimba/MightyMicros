

import math


class Detection(object):
    def __init__(self, bbox: tuple, bbox_norm: tuple, database: list):
        """Initializes a new detection instance.

        Args:
            bbox (tuple): A tuple representing the bounding box (x1, y1, x2, y2)
            bbox_norm (tuple): A tuple representing the normalized bounding box (x1, y1, x2, y2)
            database (list): A list containing all instances of detections.
        """
        
        self.bbox = bbox
        self.bbox_norm = bbox_norm
        self.neighbors = []
        self.id = -1
        self.find_neighbors(database)
        
    def assign_id(self, database: list):
        """Assigns a unique ID to the detection instance.
        """
        # Check spatial key to see if any detections within self.neighbors match up. If so, assign the same ID.
        
        # Look at each detection in database, if their neighbors align to this detection's neighbors, assign the same ID.
        is_match = False
        for i, detection in enumerate(database):
            if (is_match := self.equal(detection)):
                self.id = detection.id
                database[i] = self  # Overwrite if it is the same detection
                break

        if not is_match:
            self.id = len(database) + 1
            database.append(self)
        
    def equal(self, other: object):
        """Determines if the current detection instance is the same as another detection instance.

        Args:
            other (object): Another detection instance.

        Returns:
            bool: True if the current detection instance is the same as another detection instance, False otherwise.
        """
        # Check number of neighbors both detections have
        if len(self.neighbors) != len(other.neighbors):
            return False
        
        # Check to see if order of neighbors aligns with another detection in database.
        # If so, this detection is the same as the matched detection, this detection should override the matched detection.
        for neighbor, other_neighbor in zip(self.neighbors, other.neighbors):
            if neighbor['id'] != other_neighbor['id']:
                return False
        return True
    
    def find_neighbors(self, database: list):
        """Finds the detections that are spatially close to the current detection instance.

        Args:
            database (list): A list containing all instances of detections.
        """
        # Check spatial key to see if any detections are spatially close to the current detection instance.
        # If so, add them to self.neighbors.
        
        for detection in database:
            if self.is_neighbor(detection):
                vector, distance, angle = self.calculate_vector(detection)
                # Check to see if this detection is closer than a current neighbor. If so, replace the current neighbor.
                for i, neighbor in enumerate(self.neighbors):
                    if abs(neighbor['angle'] - angle) < math.radians(10) and distance < neighbor['distance']:
                        self.neighbors[i] = {'id': detection.id, 'bbox': detection.bbox, 'vector': vector, 'distance': distance, 'angle': angle}
                        break
                else:
                    # Loop wasn't broken, this neighbor doesn't replace an old neighbor.
                    self.neighbors.append({'id': detection.id, 'bbox': detection.bbox, 'vector': vector, 'distance': distance, 'angle': angle})
        
        self.neighbors = sorted(self.neighbors, key=lambda neighbor: neighbor['distance'])
        
        # Now that neighbors have been found, assign an ID to the current detection instance.
        self.assign_id(database)
    
    
    def is_neighbor(self, other: object):
        """Determines if the current detection instance is spatially close to another detection instance.

        Args:
            other (object): Another detection instance.

        Returns:
            bool: True if the current detection instance is spatially close to another detection instance, False otherwise.
        """
        vector, distance, angle = self.calculate_vector(other)
        # This is set to 100px for now, should be tuned more later.
        
        # Neighbor decided by 2 rules: Distance and direction. A neighbor is direct, therefore only 1 neighbor could exist within a given distance and direction. 
        # If a direction is the same as the current neighbor, but the distance is further, the detection is not a neighbor.
        
        # Check for existing neighbors, grab their angles for blacklist.
        for neighbor in self.neighbors:
            # If angle is within 10 degrees of another neighbor, and is farther away, it is not a neighbor.
            if abs(neighbor['angle'] - angle) < math.radians(10) and distance > neighbor['distance']:
                return False
        return True
    
    def calculate_vector(self, other_detection):
        """
        Calculates the vector pointing from this detection to another detection.

        Parameters:
        other_detection (Detection): Another detection instance.

        Returns:
        tuple: A tuple representing the vector (dx, dy).
        """
        dx = other_detection.bbox[0] - self.bbox[0]
        dy = other_detection.bbox[1] - self.bbox[1]
        
        vector = (dx, dy)
        distance = (dx**2 + dy**2)**0.5
        angle = math.atan2(dy, dx) # In radians
        return (vector, distance, angle)