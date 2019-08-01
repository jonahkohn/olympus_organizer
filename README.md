# Olympus Multi-acquisition Setup

### Acquisition procedure:

1. Turn on the microscope

2. Open the Scan Tracking Excel sheet, identify the slides you wish to image.

3. On the multi-slide stage, load the slides **in the same order as the excel sheet** from left to right, with the bar codes facing toward the microscope.

4. Create an overlap map:
    - Select the 2x objective.
    - Using the live imaging function, bring the leftmost slide into view.
    - Identify the top of the leftmost slide. Add an acquisition rectangle to the map as a marker.
    - Identify the bottom of the leftmost slide. Add an acquisition rectangle to the map as a marker.
    - Drag a rectangle from the top marker to the bottom marker, until it covers all of the brain sections on the slide.
    - Delete the top and bottom marker acquisitions.
    - Repeat for all other slides.

    - When finished, review the acquisition order and parameters of each overlap image.
    - **Be sure to check the "Overlap Mapping" and "Stitching" boxes, to the left of each acquisition command box.**
    - On the top right, select the MATL imaging screen and start the imaging.

5. Switch to the 10x objective. Be sure to raise the stage to avoid a collision.

5. **Using the overlap map as a guide, follow the acquisition order on the excel sheet.**

    - For each area of interest, adjust the laser intensity and z-plane parameters as necessary. Remember to update the parameters after adjusting using the "Save acquisition parameters" button.

    - After adding all areas, confirm the order of acquisition by using the overlap map and excel sheet.

    - **Be sure to select "Stitching" for each image on the list.**

6. When satisfied with each image's parameters and the order, take a screenshot of the overlay map which shows the acquisition order.

7. Make sure the destination folder and image names are satisfactory.

7. Under the MATL imaging screen, start imaging.

8. When finished, click File -> Export multiple.

    - Under target folder, select the acquired 10x images Ignore the non-stitched images, only export the stitched.

    - Choose a destination folder.

    - Export as: TIF files, with Raw Image and 16-bit settings.

9. Copy all finished cells in the excel sheet to a new excel file, including the labelled column headings.

    - Use example_sheet.xlsx as a reference for correct creation.

    - Make sure that every row has the animal ID by dragging the number down.

    - Save in the folder containing the exported TIFs.

10. Run organize.py.

    - First, select the folder containing all the TIFs.

    - Second, select the newly created excel sheet.

10. Look inside the new folder Organized.

    - Check for correctly created Stack and MIP folders, and reference log.txt with the overlay map screenshot.

11. Upload the animal ID folders to LIMS.
