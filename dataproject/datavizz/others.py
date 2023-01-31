'''
class FileDisplayView(generics.RetrieveAPIView):
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file = instance.file.path
        if file.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.endswith('.xls') or file.endswith('.xlsx'):
            data = pd.read_excel(file)
        x = None
        y = None
        for column in data.columns:
            if x is None:
                x = data[column]
            elif y is None:
                y = data[column]
            else:
                break
        if x is None or y is None:
            return Response("No suitable x and y values found in DataFrame")
        plt.plot(x, y)
        plt.show()
        return Response("data displayed")

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
'''


'''          
class FileViewSet(viewsets.ModelViewSet):
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    parser_classes = (MultiPartParser, FileUploadParser, FormParser)
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

    def perform_create(self, serializer):
        file = self.request.data['file']
        if file.size > 10485760:  # 10MB
            raise serializers.ValidationError('file must be less than 10mb')
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    # @action(detail=True, methods=['get'])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file = instance.file
        # check if file is csv or excel file
        valid_extension = ['.csv', '.xls', 'xlsx']
        if not any(file.endswith(ext) for ext in valid_extension):
            raise ValueError(
                f'file must have one of the following extensions: {", ".join(valid_extension)}')
        # use pandas to clean
        if file.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.endswith('.xls') or file.endswith('.xlsx'):
            df = pd.read_excel(file)

        # perform additional cleaning and procesing on the Dataframe
        df = df.dropna()  # remove rows with missing values
        df = df.drop_duplicates()  # removes duplicate rows
        df = df.dropna(subset=df.columns, how='all')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # @action(detail=True, methods=['get'])
    def display(self, request, *args, **kwargs):
        instance = self.get_object()
        file = instance.file.path
        if file.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.endswith('.xls') or file.endswith('.xlsx'):
            data = pd.read_excel(file)
        x = None
        y = None
        for column in data.columns:
            if x is None:
                x = data[column]
            elif y is None:
                y = data[column]
            else:
                break
        if x is None or y is None:
            return Response("No suitable x and y values found in DataFrame")
        plt.plot(x, y)
        plt.show()
        return Response("data displayed")
    '''
