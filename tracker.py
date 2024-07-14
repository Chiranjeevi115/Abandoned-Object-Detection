# DataFlair Abandoned object Tracker

import math

class ObjectTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

        self.abandoned_temp = {}

    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []
        abandoned_object = []
        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) / 2
            cy = (y + y + h) / 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                distance = math.hypot(cx - pt[0], cy - pt[1])

                if distance < 25:
                    # update the center point
                    self.center_points[id] = (cx, cy)

                    objects_bbs_ids.append([x, y, w, h, id, distance])
                    same_object_detected = True
                    

                    #   Add same object to the abandoned_temp dictionary. if the object is
                    #   still in the temp dictionary for certain threshold count then
                    #   the object will be considered as abandoned object 
                    if id in self.abandoned_temp:
                        if distance<1:
                            if self.abandoned_temp[id] >100:
                                abandoned_object.append([id, x, y, w, h, distance])
                            else:
                                self.abandoned_temp[id] += 1  # Increase count for the object
                   
                    break
            

            # If new object is detected then assign the ID to that object
            if same_object_detected is False:
                # print(False)
                self.center_points[self.id_count] = (cx, cy)
                self.abandoned_temp[self.id_count] = 1 # Add new object with initial count 1
                objects_bbs_ids.append([x, y, w, h, self.id_count, None])
                self.id_count += 1
                

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        abandoned_temp_2 = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id, _ = obj_bb_id
            center = self.center_points[object_id]
            
            new_center_points[object_id] = center

            if object_id in self.abandoned_temp:
                counts = self.abandoned_temp[object_id]
                abandoned_temp_2[object_id] = counts

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        self.abandoned_temp = abandoned_temp_2.copy()
        return objects_bbs_ids , abandoned_object



