#include "Voxelyze.h"
#include <iostream>

int main() {
    CVoxelyze Vx(0.005); //5mm voxels
    CVX_Material* pMaterial = Vx.addMaterial(1000000, 1000); //A material with stiffness E=1MPa and density 1000Kg/m^3
    CVX_Voxel* Voxel1 = Vx.setVoxel(pMaterial, 0, 0, 0); //Voxel at index x=0, y=0. z=0
    CVX_Voxel* Voxel2 = Vx.setVoxel(pMaterial, 1, 0, 0);
    CVX_Voxel* Voxel3 = Vx.setVoxel(pMaterial, 2, 0, 0); //Beam extends in the +X direction

    Voxel1->external()->setFixedAll(); //Fixes all 6 degrees of freedom with an external condition on Voxel 1
    Voxel3->external()->setForce(0, 0, -1); //pulls Voxel 3 downward with 1 Newton of force.

    //added some debugging output in this loop
    for (int i = 0; i < 1000; i++) {
        Vx.doTimeStep();
#define INFO(vox) do { \
    Vec3D<double> pos = vox->position(); \
    std::cout << "[" << #vox << ": " << pos.x << " " << pos.y; \
    std::cout << " " << pos.z << "]"; \
} while(0)
        INFO(Voxel1); INFO(Voxel2); INFO(Voxel3);
        std::cout << std::endl;
        // of course, in your real program you would use arrays
    }
}
