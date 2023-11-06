# Computer Vision Design Document

## Purpose

The purpose of this module is to accept video input and return a position to move the end effector to.

## Important Classes

### Detect

 - Initialize video input source
 - Accept video input
 - Return the ball's position in pixel space
 - Return the radius of the ball

 ### Localize

 - Accept the ball's position in pixel space
 - Accept the radius of the ball
 - Return the ball's position in the base frame

 ### Predict

 - Accept the ball's position in the base frame
 - Return where the end effector needs to be in the base frame