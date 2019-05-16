import math

def track(coordinates, detections, dimensions):
    if detections == []:
        det = coordinates
        return det
    
    det = []
    newstuff = coordinates[:]

    while True:
        if len(detections) == 0:
            break
        existing = detections[0]
        found = False
        for i, new in enumerate(coordinates):
            if new != 0:
                if get_bbox_similarity(existing['bbox'], new['bbox']):
                    if get_pose_similarity(existing, new):
                        found = True
                        if 'hidden' in existing:
                            #print('continued')
                            #output, hidden = model(new['coordinate'], existing['hidden']) --> this will be used if a hidden is already in
                            new['hidden'] = 0 #replace zero with hidden obtained
                            det.append(new)
                            coordinates[i] = 0
                            continue
                        else:
                            #print('new tracked')
                            #h = model.init_hidden
                            #output,hidden = model(exisiting['coordinate'], h) --> get the hidden state from the existing coordinates
                            #output, hidden = model(new['coordinate'], hidden)
                            new['hidden'] = 0 #replace zero with hidden obtained
                            det.append(new)
                            coordinates[i] = 0
                            continue
        if not found:
            existing['count'] += 1
            det.append(existing)
        detections.pop(0)
    coordinates = [x for x in coordinates if x != 0]
    for i in coordinates:
        det.append(i)
        det = [x for x in det if x['count']<5]
    return det

def get_pose_similarity(existing, new):
    xyxy = new['dimensions']
    diagonal = 0.1 * math.sqrt((xyxy[2]-xyxy[0])**2 + (xyxy[3]-xyxy[1])**2)
    similarity = []
    new = new['coordinate']
    existing = existing['coordinate']
    for i in range(16):
        if existing[i][0] == 0 and existing [i][1] == 0:
            continue
        if new[i][0] == 0 and new[i][1] == 0:
            continue
        joint_diff = math.sqrt((abs(new[i][0]-existing[i][0]))**2 + abs(new[i][1]-existing[i][1])**2)
        if joint_diff >= diagonal:
            similarity.append(0)
        else:
            similarity.append((1-(joint_diff/diagonal)))
    if len(similarity) == 0:
        return False
    score = sum(similarity)/len(similarity)
    if score >= 0.15:
        print('similar skeleton')
        return True
    else:
        print('different skeleton')
        return False

def get_bbox_similarity(existing, new):
    if existing == new:
        return True
    difference = 0
    for i in range(4):
        difference += abs(existing[i]-new[i])
    if difference > 0.2:
        return False
    return True
    

def relative_bbox(xyxy, dimensions):
    x0 = xyxy[0].item()/dimensions[0]
    x1 = xyxy[2].item()/dimensions[0]
    y0 = xyxy[1].item()/dimensions[1]
    y1 = xyxy[3].item()/dimensions[1]
    return [x0, x1, y0 ,y1]