#include <opencv2/opencv.hpp>
#include <iostream>


using namespace cv;
using namespace std;

/** Global variables */
string window_name = "My Camera Feed";
String face_cascade_name = "haarcascade_frontalface_alt.xml";
String eyes_cascade_name = "haarcascade_eye_tree_eyeglasses.xml";
CascadeClassifier face_cascade;
CascadeClassifier eyes_cascade;

/** Function Headers */
void detectAndDisplay( Mat frame );

int main(int argc, char* argv[])
{
      //-- 1. Load the cascades
    if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };
    if( !eyes_cascade.load( eyes_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };

    //Open the default video camera
    VideoCapture cap(0);

    // if not success, exit program
    if (cap.isOpened() == false)  {
        cout << "Cannot open the video camera" << endl;
        cin.get(); //wait for any key press
        return -1;
    } 

    namedWindow(window_name); //create a window called "My Camera Feed"
    moveWindow(window_name, 20,20);
    while (true){
        Mat frame;
        bool bSuccess = cap.read(frame); // read a new frame from video 

        //Breaking the while loop if the frames cannot be captured
        if (bSuccess == false) 
        {
        cout << "Video camera is disconnected" << endl;
        cin.get(); //Wait for any key press
        break;
        }

        detectAndDisplay(frame);
        //show the frame in the created window
        imshow(window_name, frame);

        //wait for for 10 ms until any key is pressed.  
        //If the 'Esc' key is pressed, break the while loop.
        //If the any other key is pressed, continue the loop 
        //If any key is not pressed withing 10 ms, continue the loop 
        if (waitKey(10) == 27)
        {
        cout << "Esc key is pressed by user. Stopping the camera" << endl;
        break;
        }
    }

    return 0;
}

void detectAndDisplay( Mat frame ){
    std::vector<Rect> faces;
    Mat frame_gray;

    cvtColor(frame, frame_gray, COLOR_BGR2GRAY);
    equalizeHist( frame_gray, frame_gray );

    //-- Detect faces
    face_cascade.detectMultiScale(frame_gray, faces, 1.1, 2, 0 | CASCADE_SCALE_IMAGE, Size(30, 30));

    for( size_t i = 0; i < faces.size(); i++ )
    {
    Point center( faces[i].x + faces[i].width*0.5, faces[i].y + faces[i].height*0.5 );
    ellipse( frame, center, Size( faces[i].width*0.5, faces[i].height*0.5), 0, 0, 360, Scalar( 255, 0, 255 ), 4, 8, 0 );

    Mat faceROI = frame_gray( faces[i] );
    std::vector<Rect> eyes;

    //-- In each face, detect eyes
    eyes_cascade.detectMultiScale(faceROI, eyes, 1.1, 2, 0 | CASCADE_SCALE_IMAGE, Size(30, 30));

    for( size_t j = 0; j < eyes.size(); j++ )
        {
        Point center( faces[i].x + eyes[j].x + eyes[j].width*0.5, faces[i].y + eyes[j].y + eyes[j].height*0.5 );
        int radius = cvRound( (eyes[j].width + eyes[j].height)*0.25 );
        circle( frame, center, radius, Scalar( 255, 0, 0 ), 4, 8, 0 );
        }
    }
    //-- Show what you got
    imshow( window_name, frame );
}