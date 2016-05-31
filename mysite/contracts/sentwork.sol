// contract sentwork {
//     create_and_construct.featsets();
// }  





contract create_and_construct {
    
    uint workdone;
    
    struct constituent {
        string username;
        uint worklog;
    }

    struct featset {
        uint clustrId;
        uint dist;
        uint[] featfreq;
    }

    enum states {init, trainset, featset} 
    states state;

    string[] reviews;
    string[] trainset;
    string[] features;
    featset[] public featsets;
    
    mapping(address => constituent) public constituents;
    
    
    function init(address to) {
        if (to == msg.sender || msg.sender.balance < this.balance) throw;
        to.send(this.balance);
        state = states.init;
    }
    
    function create_trainset() {
        if (state != states.init) throw;
        var numreviews = reviews.length;
        var hashnum = block.blockhash(1) ^ msg.sender << block.difficulty;
        var idx = hashnum % numreviews;
        var trainsize = int((hashnum + 1) * numreviews / (hashnum + 2));
        for (var count = 0; count < trainsize; count ++) {
            trainset[count] = reviews[idx];
            idx ++;
            if (idx >= numreviews) idx = 0;
        }
        state = states.trainset;
    }
    
    function construct_featsets() {
        if (state != states.trainset) throw;
        // find 2500 most common word and 500 most common bigram features
        // find feature frequencies in each review
        // compile list of frequency featuresets
        for (var idx = 0; idx < featsets.length; idx++) {
            featsets[idx].clustrId = idx;
        }
        state = states.featset;
        return(1); 
    }
    
    
}








contract clustr {
    
    uint workdone;
    
    struct constituent {
        string username;
        uint worklog;
    }
    
    struct featset {
        uint clustId;
        mapping(string => uint) featfreq;
    }
    
    enum states {iter, sent}
    states state;
    
    featset[] featsets;
    mapping(address => constituent) public constituents;
    
    function iter() {
        // Perform one iteration of clustering
        var hashnum = block.number ^ msg.value << block.gasLimit();
        var minclusters = hashnum % 9;
        var idx = hashnum % featsets.length;
        var fs = featsets[idx];
        var clustrId = fs.clustrId;
        var clustrMembers = [idx];
        for (var i = 0; i < featsets.length; i++) {
            if (i == idx) continue;
            if (featsets[i].clustrId == clustrId) clustrMembers.push(i);
        }
        var clustrMember;
        var inclustr;
        var closest = 10000000000;
        var dist;
        var nn;
        var pseudorand1;
        var pseudorand2;
        var nearestNeighbors = [];
        var alreadyNeighbor;
        var nn2;
        var highest;
        var clustr;
        var nbr;
        mapping(uint => uint) count;
        for (var j = 0; j < featsets.length; j++) {
            inclustr = false;
            for (var k = 0; k < clustrMembers.length; k++) {
                clustrMember = clustrMembers[k];
                if (j == clustrMember) {
                    inclustr = true;
                    break;
                }
            }
            if (inclustr) continue;
            dist = 0;
            for (var l = 0; l < clustrMembers.length; l++) {
                clustrMember = clustrMembers[l];
                for (var m = 0; m < featsets[j].featfreq.length; m++) dist += (featsets[j].featfreq[m] - featsets[clustrMember].featfreq[m]) ** 2;
            }
            if (dist < closest) {
                closest = dist;
                nn = j;
            }
        }
        if (featsets[nn].dist >= 0 && featsets[nn].clustrId != -1) {
            if (featsets[nn])
            pseudorand1 = hashnum % featsets[nn].dist;
            pseudorand2 = hashnum % closest;
            if (pseudorand1 < featsets[nn].dist && pseudorand2 > closest) {
                featsets[nn].clustrId = clustrId;
                featsets[nn].dist = closest;
            }
            else if (pseudorand1 > featsets[nn].dist && pseudorand2 > closest) featsets[nn].clustrId = -1; 
        }
        else if (featsets[nn].dist >= 0 && featsets[nn].clustrId == -1) {
            for (var n = 0; n < 10; n++) {
                closest = 10000000000;
                for(var o = 0; o < featsets.length; o++) {
                    if (featsets[o].clustrId == -1) continue;
                    alreadyNeighbor = false;
                    for (var p = 0; p < nearestNeighbors.length; p++) {
                        if (nearestNeighbors[p] == o) {
                            alreadyNeighbor = true;
                            break;
                        }
                    }
                    if (alreadyNeighbor) continue;
                    dist = 0;
                    for (var q = 0; q < featsets[nn].featfreq.lenth; q++) dist += (featsets[nn].featfreq[q] - featsets[o].featfreq[q]) ** 2;
                    if (dist < closest) {
                        closest = dist;
                        nn2 = o;
                    }
                }
                nearestNeighbors.push(nn2);
            }
            for (var r = 0; r < nearestNeighbors.length; r++) count[featsets[nearestNeighbors[r]].clustrId] += 1;
            highest = 0;
            for (var s = 0; s < nearestNeighbors.length; s++) {
                nbr = nearestNeighbors[s];
                if (count[featsets[nbr].clustrId] > highest) {
                    highest = count[featsets[nbr].clustrId];
                    clustr = featsets[nbr].clustrId;
                }
            }
            featsets[nn].clustrId = clustr; 
        }
        else {
            featsets[nn].clustrId = clustrId;
            featsets[nn].dist = closest;
        }
    }
    
    function send(address to) { 
        if (to == msg.sender) throw;
        send(to, featsets);
        state = states.sent;
    }

    
    
}




















contract classify {
    mapping(uint => featset) clustrfeatfreqs;
    uint[] totalfeatfreqs;
    mapping(uint => string[]) labels;
}
