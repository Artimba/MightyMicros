import numpy as np
from torch import Tensor
from pykalman import KalmanFilter as PyKalmanFilter

# Step 1. Define State and Measurement Threshold
# State = [x,y,v_x,v_y]^T

# Step 1.a. Define Measurement vector
# Measurement = [x_obs,y_obs]^T

class KalmanFilter(object):
    def __init__(self, bbox_norm: Tensor, delta_t: float):
        
        # region [ Step 1: Initialize State Vector ]
        centroid = self.calculate_centroid(bbox_norm)
        
        state_vector = np.array([centroid[0], centroid[1], 0, 0])
        # endregion
        
        # region [ Step 2: State Transition Model ]
        # Look at this in terms of the submatrices. 
        # The upper left 2x2 refers to the position (old x y), when applied with the next submatrix, it will yield the new position (new x y).
        # The upper right 2x2 is the second part of updating the position, taking into account the velocity given a delta t,
        # The bottom right 2x2 represents the velocity change / acceleration. This is constant in this case, so the 1's copy the previous velocities to the next state.
        state_matrix = np.array([[1, 0, delta_t, 0],
                                [0, 1, 0, delta_t],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])
        
        # For any state represented as [x,y,v_x,v_y]^T, this state matrix will yield the next state based off the assumption of constant velocity.
        # endregion
        
        # region [ Step 3: Define Observation Model ]
        # Observation matrix extracts the position from the state vector.
        observation_matrix = np.array([[1, 0, 0, 0],
                                    [0, 1, 0, 0]])
        # endregion
        
        # region [ Step 3.a: Noise]
        # TODO: Tune these values to fit our system
        # If measurements are noisy, increase the values of sigma_x and sigma_y.
        # If measurements are overfitting, decrease the values of sigma_x and sigma_y.
        sigma_x = 0.5
        sigma_y = 0.5
        
        measurement_noise = np.array([[sigma_x**2, 0],
                                    [0, sigma_y**2]])
        
        # Error Covariance Matrix (4x4)
        # TODO: This is set very high to start. Tune this value to fit our system.
        error_covariance_matrix = np.eye(4) * 500
        
        # Process Noise Covariance Matrix (4x4)
        q = 0.1 # TODO: Tune this value to fit our system.
        process_noise_covariance_matrix = np.eye(4) * q
        
        # endregion
        
        # region [ Step 4: Initialize Kalman Filter ]
        
        # I was going to make a completely custom KalmanFilter, then I peeked at the pykalman source code and said "nope".
        self.kalman = PyKalmanFilter(transition_matrices=state_matrix,
                            observation_matrices=observation_matrix,
                            transition_covariance=process_noise_covariance_matrix,
                            observation_covariance=measurement_noise,
                            initial_state_mean=state_vector,
                            initial_state_covariance=error_covariance_matrix)
        
        # Save the needed estimates for later prediction.
        self.current_state_estimate = state_vector
        self.current_covariance_estimate = error_covariance_matrix
        
        # endregion
    
    def predict(self):
        # Predict the next state.
        self.current_state_estimate, self.current_covariance_estimate = self.kalman.filter_update(self.current_state_estimate, 
                                                                                                  self.current_covariance_estimate)
        
        # Return the predicted state. Format is [x,y,v_x,v_y]^T
        return self.current_state_estimate

    def update(self, bbox_norm: Tensor):
        # Update the measurement vector.
        x1, y1, x2, y2 = bbox_norm[:4]
        centroid = self.calculate_centroid(bbox_norm)
        measurement_vector = np.array([centroid[0], centroid[1]])
        
        # Update the state estimate.
        self.current_state_estimate, self.current_covariance_estimate = self.kalman.filter_update(self.current_state_estimate, 
                                                                                                  self.current_covariance_estimate, 
                                                                                                  observation=measurement_vector)
        
        # Return the updated state. Format is [x,y,v_x,v_y]^T
        return self.current_state_estimate

    def calculate_centroid(self, bbox: Tensor):
        # bbox can either be normalized or not for this, doesn't matter. HOWEVER, the rest of the code assumes normalized bboxes.
        
        x1, y1, x2, y2 = [int(coord) for coord in bbox]
        centroid = np.array([(x1 + x2) / 2, (y1 + y2) / 2])
        return centroid


# region [ Old code ]
# def kalman(current_bbox_norm: Tensor, previous_bbox_norm: Tensor, delta_t: float):
    
#     # region [ Step 1: State and Measurement Threshold ]
#     # delta_t is reciprocal of FPS. i.e 30 FPS would be delta_t = 1/30
#     curr_x1, curr_y1, curr_x2, curr_y2 = current_bbox_norm[:4]
#     current_centroid = np.array([(curr_x1 + curr_x2) / 2, (curr_y1 + curr_y2) / 2])
    
#     if previous_bbox_norm is None:
#         print('Previous_bbox_norm is None. Assuming initial state')
#         state_vector = np.array([current_centroid[0], current_centroid[1], 0, 0])
#     else:
#         prev_x1, prev_y1, prev_x2, prev_y2 = previous_bbox_norm[:4]
#         previous_centroid = np.array([(prev_x1 + prev_x2) / 2, (prev_y1 + prev_y2) / 2])
#         v_x = (current_centroid[0] - previous_centroid[0]) / delta_t
#         v_y = (current_centroid[1] - previous_centroid[1]) / delta_t
#         state_vector = np.array([current_centroid[0], current_centroid[1], v_x, v_y])
    
#     # endregion
    
#     # region [ Step 2: State Transition Model ]
#     # Look at this in terms of the submatrices. 
#     # The upper left 2x2 refers to the position (old x y), when applied with the next submatrix, it will yield the new position (new x y).
#     # The upper right 2x2 is the second part of updating the position, taking into account the velocity given a delta t,
#     # The bottom right 2x2 represents the velocity change / acceleration. This is constant in this case, so the 1's copy the previous velocities to the next state.
#     state_matrix = np.array([[1, 0, delta_t, 0],
#                             [0, 1, 0, delta_t],
#                             [0, 0, 1, 0],
#                             [0, 0, 0, 1]])
    
#     # For any state represented as [x,y,v_x,v_y]^T, this state matrix will yield the next state based off the assumption of constant velocity.
#     # endregion
    
#     # region [ Step 3: Define Observation Model ]
#     # Observation matrix extracts the position from the state vector.
#     observation_matrix = np.array([[1, 0, 0, 0],
#                                    [0, 1, 0, 0]])
#     # endregion
    
#     # region [ Step 3.a: Noise]
#     # TODO: Tune these values to fit our system
#     # If measurements are noisy, increase the values of sigma_x and sigma_y.
#     # If measurements are overfitting, decrease the values of sigma_x and sigma_y.
#     sigma_x = 0.5
#     sigma_y = 0.5
    
#     measurement_noise = np.array([[sigma_x**2, 0],
#                                   [0, sigma_y**2]])
    
#     # Error Covariance Matrix (4x4)
#     # TODO: This is set very high to start. Tune this value to fit our system.
#     error_covariance_matrix = np.eye(4) * 500
    
#     # Process Noise Covariance Matrix (4x4)
#     q = 0.1 # TODO: Tune this value to fit our system.
#     process_noise_covariance_matrix = np.eye(4) * q
    
#     # endregion
    
#     # region [ Step 4: Initialize Kalman Filter ]
    
#     # I was going to make a completely custom KalmanFilter, then I peeked at the pykalman source code and said "nope".
#     kalman = KalmanFilter(transition_matrices=state_matrix,
#                           observation_matrices=observation_matrix,
#                           transition_covariance=process_noise_covariance_matrix,
#                           observation_covariance=measurement_noise,
#                           initial_state_mean=state_vector,
#                           initial_state_covariance=error_covariance_matrix)
    
#     # endregion
# endregion
    
    
    
    
    
    