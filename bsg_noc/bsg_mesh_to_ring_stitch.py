#!/usr/bin/python

#
# bsg_mesh_to_ring_stitch
#
# this module uses space filling curves to organize
# a mesh of items into a ring of nearest-neighbor connections
#
# because of geometry, both X and Y coordinates cannot be odd
#
#

topX = 8
topY = 8

print "// bsg_mesh_to_ring_coord"
print "// maps an X,Y coordinate to an address on a ring"
print "// ";

print "module bsg_mesh_to_ring_stitch   #(parameter  y_max_p=-1"
print "                                  ,parameter x_max_p=-1"
print "                                  ,parameter width_back_p = -1"
print "                                  ,parameter width_fwd_p  = -1"
print "                                  ,parameter b_lp = $clog2(x_max_p*y_max_p)"
print "                                  ) (output  [x_max_p-1:0][y_max_p-1:0][b_lp-1:0] id_o"
print "                                     ,output [x_max_p-1:0][y_max_p-1:0][width_back_p-1:0] back_data_in_o"
print "                                     ,input  [x_max_p-1:0][y_max_p-1:0][width_back_p-1:0] back_data_out_i"
print "                                     ,output [x_max_p-1:0][y_max_p-1:0][width_fwd_p-1:0]  fwd_data_in_o"
print "                                     ,input  [x_max_p-1:0][y_max_p-1:0][width_fwd_p-1:0]  fwd_data_out_i"
print "                                    );\n\n"


def print_config (maxX,maxY,order) :
        matrix = [[0 for y in range(maxY)] for x in range(maxX)]
        my_dict = dict();
        for position,(x,y) in enumerate(order) :
            my_dict[position] = (x,y);
            matrix[x][y] = position;

        print "if (x_max_p ==",maxX," && y_max_p ==",maxY,")\nbegin\n"
        for y in range(maxY-1,-1,-1) :
            for x in range(maxX-1,-1,-1) :
                position=matrix[x][y];
                below = maxX*maxY-1  if ((position - 1) < 0) else position - 1;
                above = 0 if ((position + 1) == maxX*maxY) else position + 1;
                (below_x,below_y)=my_dict[below];
                (above_x,above_y)=my_dict[above];
                print "assign back_data_in_o[",below_x,"][",below_y,"] = back_data_out_i[",x,"][",y,"]; // ",below,"<-",position
                print "assign fwd_data_in_o [",above_x,"][",above_y,"] = fwd_data_out_i [",x,"][",y,"]; // ",position,"->",above
        print "\n"
        print " assign id_o = \n {"
        print "// y = ",
        for y in range(0,maxY) :
            print str(y)+", ",
        print "";
        for x in range(0,maxX) :
            print "  {",
            for y in range(0,maxY) :
                if (y != 0) :
                        print ",",
                print "b_lp ' (" + str(matrix[x][y]) +")",
            if (x != maxX-1) :
                    print "    }, // x = ",x
            else:
                    print "    } // x = ",x
        print " };\nend\n"

# even X, odd/even Y
for maxX in range(2,topX+1,2) :
    for maxY in range(2,topY+1,1) :
        order=[]
        for x in range(0,maxX,2) :
            for y in range(1,maxY,1) :
                order.append( (x,y))
            for y in range(maxY-1,0,-1) :
                order.append( (x+1,y))

        for x in range(maxX-1,-1,-1) :
            order.append((x,0))

        print_config(maxX,maxY,order)

# odd X, even Y
for maxX in range(3,topX+1,2) :
    for maxY in range(2,topY+1,2) :
        order=[]
        for y in range(0,maxY,2) :
            for x in range(1,maxX,1) :
                order.append( (x,y))
            for x in range(maxX-1,0,-1) :
                order.append( (x,y+1))

        for y in range(maxY-1,-1,-1) :
            order.append((0,y))

        print_config(maxX,maxY,order)

# handle 1x2
print_config(1,2,[(0,0), (0,1)]);
print_config(2,1,[(0,0), (1,0)]);

print "initial assert ((x_max_p <= " + str(topX) + ") && (y_max_p <= " + str(topY) +")) else begin $error(\"%m x_max_p %d or y_max_p %d too large; rerun generator with larger size than %d/%d\",x_max_p,y_max_p,"+str(topX)+","+str(topY)+"); $finish(); end "


print "endmodule"
