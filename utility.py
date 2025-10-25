def normalizedLandmark_to_numpyLocationVector(lm):
    import numpy as np
    
    return np.array([lm.x, lm.y, lm.z], dtype=np.float32)
