#include "Voxelyze.h"
#include <iostream>
#include <string.h>


/***********Notes for Group***************/
//Need some way to know how long the handle
//is at the bottom
/*****************************************/

#define FORCE_PARAM_TOTAL 5

//split the entire string into an array of floats
//note: first two arguments are integers but we can type cast
float* split(const char* array)
{
    std::string conversion = "";
    int strLength = strlen(array);
    float* floatArray = new float[FORCE_PARAM_TOTAL]; //5 argument parameters (row index | col index | force 1 | force 2 | force 3)
    int arrayIndex = 0; int i = 0;
    while (arrayIndex < FORCE_PARAM_TOTAL)
    {
        //printf("%c\n", array[i]); //we somehow access null here
        if (array[i] != ' ')
            conversion = conversion + array[i];
        else
        {
            const char* string = conversion.c_str();
            //printf("%s\n", string);
            float value = atof(string);
            floatArray[arrayIndex] = value;
            arrayIndex++;
            conversion = "";
        }
        i++;
    }
    return floatArray;
}

int main() {
    std::string line;
    int lineCount = 0;
    int r, c, handleSize;
    int** matrix;
    CVX_Voxel*** voxMatrix;


    //These two things will need to be edited for the correctness of metamaterial properties
    CVoxelyze Vx(.005); //set size to 5mm voxels
    CVX_Material* pMaterial = Vx.addMaterial(1000000, 1000); //A material with stiffness E=1MPa and density 1000Kg/m^3

    //parse the information from the file
    while ( std::getline(std::cin, line) )
    {
        if ( !line.empty() )
        {
            const char* arr = line.c_str();
            int strLength = strlen(arr);
            //get number of bytes to allocate for the rows of the matrix
            if ( lineCount == 0 )
            {
                r = atoi(arr);
                lineCount++;
            }
            //get the number of bytes to allocate for the columns of the matrix
            else if ( lineCount == 1 )
            {
                c = atoi(arr);
                lineCount++;
            }
            else if ( lineCount == 2 )
            {
                handleSize = atoi(arr);
                lineCount++;
            }
            //create and set the voxel matrix
            else if ( lineCount >= 3 && lineCount < r+3 )
            {
                //initialize a new matrix for the voxel mapping (numbers and actual voxels)
                if ( lineCount == 3 )
                {
                    matrix = new int*[r];
                    for ( int i = 0; i < r; i++)
                        matrix[i] = new int[c]; 
                    voxMatrix = new CVX_Voxel**[r];
                    for (int i = 0; i < r; i++)
                        voxMatrix[i] = new CVX_Voxel*[c];                  
                }

                //set the voxels in the matrices
                for ( int i = 0; i < strLength; i++ )
                {
                    matrix[lineCount-3][i] = arr[i]; //set the values of the matrix
                    voxMatrix[lineCount-3][i] = Vx.setVoxel(pMaterial, lineCount-3, i, 0); //material state, x, y, z
                    //std::cout << arr[i] << " ";
                }
                lineCount++;
                //printf("We initialized the matrix\n");
            }
            //set forces for each of the specified voxels
            else
            {
                //printf("Do we ever try to set the forces?\n");
                //get index and force values of voxels
                float* array = split(arr); //NEVER tested this method lol
                //for (int i = 0; i < 5; i++)
                //    printf("%f, ", array[i]);
                //printf("\n");
                int rVal = (int)array[0];
                int cVal = (int)array[1];
                //get the voxel from the matrix
                CVX_Voxel* vox = voxMatrix[rVal][cVal];
                //if the voxel is not null
                if ( vox != nullptr )
                {
                    //apply force to voxel
                    vox->external()->setForce(array[2], array[3], array[4]);
                }
                //printf("Debug: We set the forces\n");
            }
            //std::cout << "\n";
        }
    }

    //make bottom handle fixed (located at last row in matrix)
    int colIndex = 0;
    CVX_Voxel* vox = voxMatrix[r-1][colIndex];
    while ( colIndex < handleSize )
    {
        //make voxel stagnant
        vox->external()->setFixedAll();
        colIndex++;
        vox = voxMatrix[r-1][colIndex];
    }

    //run simulation
    for (int i = 0; i < 1000; i++) 
    {
        //take one time iteration to see change in voxels
        Vx.doTimeStep();
        //printout information
        #define INFO(vox) do { \
        Vec3D<double> pos = vox->position(); \
        std::cout << pos.x << "," << pos.y; \
        std::cout << "," << pos.z << ";"; \
        } while(0)
        //get formatted printout information for each voxel
        for (int row = 0; row < r; row++)
        {
            for(int col = 0; col < c; col++)
            {
                CVX_Voxel* temp = voxMatrix[row][col];
                if ( temp != nullptr )
                    INFO(temp); 
            }
        }
        //printout
        std::cout << std::endl;  
        //exit(0);   
    }


}
