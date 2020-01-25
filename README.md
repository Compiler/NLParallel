# NLParallel
This project wasn't planned or structured correctly. Just a spur of the night idea and it became a bit bigger than the initial prototype and thus, it's not easy to understand the code. 

This will take two topics and "connect" them by my means of connection. It uses machine learning to attempt and making the output more conhesive and the plan is to continue the intelligence towards how the connections develop. 

To search the connection graph I used a research paper with O(nlogloglogn) runtime for the two nodes (I forget the exact runtime but its weird and not a normal algorithm) but because the intention was to use cloud computing, the space complexity is much larger.


Connect any two topics and create a coherent sentence using NLP to find the connection.

Ex: Connect Computer Science and World War II. 
"Computer science is the study of the theory, experimentation, and engineering that form the basis for the design and use of computers, and not limited to Computer graphics(a sub field). Computer Graphics encompasses two-dimensional graphics and image processing-- which utilizes techniques such as super-resolution imaging (enhancement of image quality.) This requires using Imaging sensors that detect and convey information of an image. Analog sensors for invisible radiation
in the equipment tend to involve vacuum tubes of various kinds. These vacuum tubes controls electric current between electrodes in an evacuated container. This is helpful for imaging because it uses phosphor that exhibits the phenomenon of luminescence-- this helps with detecting pixels or other light sources. The most common uses of phosphors are in CRT displays and fluorescent lights. CRT phosphors were standardized beginning around World War II and designated by the letter "P" followed by a number."

![3 deep](https://github.com/Compiler/NLParallel/blob/master/NetworkData/NetworkSIFData/graphBrain_3.sif.png)

maxed unbatched search
![5 deep](https://github.com/Compiler/NLParallel/blob/master/NetworkData/NetworkSIFData/graphBrain.sif_1.png)
