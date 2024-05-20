# the compiler to use
CC = clang

# compiler flags:
#  -g    adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings
CFLAGS = -ferror-limit=1 -gdwarf-4 -ggdb3 -O0 -std=c11 -Wall -Werror -Wextra -Wno-gnu-folding-constant -Wno-sign-compare -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-variable -Wshadow

  
# files to link:
LDLIBS = -lcrypt -lcs50 -lm

# the name to use for both the target source file, and the output file:
TARGET = hello
  
all: $(TARGET)
  
$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).c $(LFLAGS)



# if more than one source use this:
# EXE = foo

# SRCS = foo.c bar.c
# OBJS = $(SRCS:.c=.o)


# $(EXE): $(OBJS)
#      $(CC) $(CFLAGS) -o $@ $(OBJS) $(LDLIBS)