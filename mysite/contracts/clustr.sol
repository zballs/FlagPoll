contract clustr {
    
    struct featset {
        uint id;
        uint[] freqs;
    }

    struct nearestNeighbor {
        uint clustrId;
        uint dist;
        bool hit;
    }
    
    struct point {
        uint clustrId;
        uint dist;
    }
    
    featset[] featsets;
    uint[] clustrIds;
    uint[] uniqueIds;
    uint closest;
    uint distance;
    uint[] clustrMembers;
    uint clustrMember;
    bool inclustr;
    uint prevNumClustrs;
    uint prevIterClustrs;
    uint[] contested;
    
    mapping(uint => nearestNeighbor) nearestNeighbors;
    
    function find_unique() {
        uniqueIds.length = 0;
        bool found;
        for (var idx = 0; idx < clustrIds.length; idx++) {
            found = false;
            for (var idx2 = 0; idx2 < uniqueIds.length; idx2++) {
                if (clustrIds[idx] == uniqueIds[idx2]) {
                    found = true;
                    break;
                }
            }
            if (!found) uniqueIds.push(clustrIds[idx]);
        }
    }

    function find_nn(uint clustrId) {

    }
    
    function contested_agglomerging(uint minclusters) {
        
        for (var idx = 0; idx < featsets.length; idx++) {
            clustrIds.push(idx);
        }
        
        // Set lengths of arrays
        uniqueIds.length = clustrIds.length;

        // Initialize number of clusters
        prevNumClustrs = clustrIds.length;
        prevIterClustrs = clustrIds.length;

        var iters = 1;
        
        while (uniqueIds.length > minclusters) {
            
            // Iterate through clusters
            for (var i = 0; i < uniqueIds.length; i++) {
                
                // Find unique cluster ids 
                find_unique();
                
                // Break if we have reached terminal number of clusters
                if (uniqueIds.length == minclusters) break;
                
                var uclustr = uniqueIds[i];
                clustrMembers.length = 0;
                
                // Find cluster members
                for (var j = 0; j < clustrIds.length; j++) {
                    var clustr = clustrIds[j];
                    if (uclustr == clustr) clustrMembers.push(j);
                }
                
                // If no cluster members, continue
                if (clustrMembers.length == 0) continue;
                
                closest = 10000000000;

                for (var iter = 0; iter < iters; iter ++) {
                
                    // Find nearest neighbor
                    for (var k = 0; k < featsets.length; k++) {
                        inclustr = false;
                        for (var l = 0; l < clustrMembers.length; l++) {
                            clustrMember = clustrMembers[l];
                            if (clustrMember == k) {
                                inclustr = true;
                                break;
                            }
                        }
                        if (inclustr) continue;
                        distance = 0;
                        for (var m = 0; m < clustrMembers.length; m++) {
                            clustrMember = clustrMembers[m];
                            for (var n = 0; n < featsets[k].freqs.length; n++) {
                                distance += (featsets[k].freqs[n] - featsets[clustrMember].freqs[n]) * (featsets[k].freqs[n] - featsets[clustrMember].freqs[n]);
                            }
                        } 
                        if (distance < closest) {
                            closest = distance;
                            var nn = k;
                        }
                    }
                        
                    // If nearest neighbor in another cluster...
                    if (nearestNeighbors[nn].hit) {
                        distance = nearestNeighbors[nn].dist;
                        var total = closest + distance;
                        var hashnum = uint(sha3(msg.sender)) << msg.gas ^ msg.value;
                        var pseudorand1 = uint((hashnum % distance) * (distance / total));
                        var pseudorand2 = uint((hashnum % closest) * (closest / total));
                        
                        if (pseudorand2 < pseudorand1) {
                            nearestNeighbors[nn].clustrId = i;
                            nearestNeighbors[nn].dist = closest;
                            clustrIds[nn] = i;
                            break;
                        }
                        

                        /* Generate 2 randnums, if closest/total < rand1 and
                        distance/total > rand2, add point to cluster... If both >
                        randnums, look at nearest neighbors of contested point...
                        Else find next closest point to cluster */
                        
                    }
                    
                    else {
                        nearestNeighbors[nn].clustrId = i;
                        nearestNeighbors[nn].dist = closest;
                        nearestNeighbors[nn].hit = true;
                        clustrIds[nn] = i;
                        break;
                    }
                }



            }
        }
    }
}