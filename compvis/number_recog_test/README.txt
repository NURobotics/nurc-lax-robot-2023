MAINTENANCE 4/16/23

To Damien:

I've found that the basic code I had been using to test out the object
detector, cvzone_real_time_detector.py, no longer works from my base PC...
and I don't know why. I suspect some libraries have changed since Summer 2021.

The code still works inside the Conda environment where I originally ran the
code, however. To run the code (which is based on the Streamlit app environment),
do the following:

- download Anaconda/Miniconda3 shell
- pip install streamlit
- run "conda create -n <environment-name-here> --file req.txt": to make a Conda
	environment that mimics the library versions I was using in July 2021.
- run "conda activate <environment-name-here>" to enter the Conda environment
	you have created
- run "streamlit run od_demo.py" to run the code within the Streamlit app.

When I activated the code this way, I got the object detector up and running.
I imagine if you replace the weights with the different model you're looking
at, we can test whether or not the h5-to-pbtext conversion works.