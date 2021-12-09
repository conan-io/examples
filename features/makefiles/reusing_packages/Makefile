SRC = src/app.cpp
OBJ = $(SRC:.cpp=.o)
OUT = src/app
INCLUDES = -I.

.SUFFIXES: .cpp

default: $(OUT)

.cpp.o:
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

$(OUT): $(OBJ)
	$(CXX) -o $(OUT)  $(OBJ)  $(LDFLAGS)  $(LIBS) 
